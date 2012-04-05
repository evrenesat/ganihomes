# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_exempt
from odeme.estbank import ESTBank
from paypal.pro.models import PayPalNVP
from places.models import Place, Currency, Booking, Transaction
from django.http import HttpResponseRedirect, HttpResponse
from  django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import logging
from utils.cache import kes
from utils.mail2perm import mail2perm
from website.views import send_message
from website.models.dil import Ceviriler
log = logging.getLogger('genel')
from datetime import datetime
from paypal.pro.views import PayPalPro



def get_booking(rq):
    return Booking.objects.get(pk=rq.session['booking_id']) if rq.session.get('booking_id') else False

def set_booking(rq, bk):
    rq.session['booking_id'] = bk.id



def get_tl_currency_code():
    tkod = kes('tl_para_kod')
    return tkod.g() or tkod.s(Currency.objects.filter(name='TRY', active=True).values_list('id',flat=True)[0])



def complete_reservation(request, booking, user_message=_('Your booking request has been successfully sent to the host.')):
    booking.set_reservation()
    booking.save()
    mail2perm(booking, url=reverse('admin:places_booking_change', args=(booking.id, )))
    booking.send_booking_request(request)
    messages.success(request, user_message)
    return HttpResponseRedirect('%s?showBookingRequest=%s'% (reverse('dashboard'), booking.id))

def bank_transfer_complete(request):
    booking = get_booking(request)
    booking.payment_type = 3
    booking.status = 8
    user_message = Ceviriler.cevir( 'rezervasyon kaydedildi.evsahibi odemeden sonra haberdar edilecek', request.LANGUAGE_CODE)
    return complete_reservation(request, booking, user_message)


def paypal_complete(request):
    booking = get_booking(request)
    paypal_transaction = PayPalNVP.objects.get(method="DoExpressCheckoutPayment",ack='Success',custom=str(booking.id))
    booking.payment_type = 2
    booking.status = 10
    return complete_reservation(request, booking)


def paypal_cancel(request):
    return render_to_response('paypal-cancel.html',{}, context_instance=RequestContext(request))

@csrf_exempt
def cc_success(request):
    context= request.session.get('booking_context',{})
    booking = get_booking(request)
    dt = request.POST
    status = int(dt.get('mdStatus',0))
    if status < 5:
        bank_pos = Transaction.get_bank(request)
        tl_ucret = booking.currency.convert_to(booking.guest_payment, get_tl_currency_code())
        bilgiler = {'xid':dt['xid'] ,'eci':dt['eci'], 'cavv':dt['cavv'],
                    'cvc':'','cardno':dt['md'], 'tutar':'',
                    'oid':booking.id, 'ip':request.META['REMOTE_ADDR'],
                    'type':'Auth'}
        basarilimi, sonuc, xml_sonuc = bank_pos.request(bilgiler)
        if basarilimi:
            trns = Transaction.objects.create(content_object=booking, type=2,
                status=10, receiver_type=40, sender_type=20,
                amount=tl_ucret, user=request.user, details=xml_sonuc)
            booking.payment_type = 1
            booking.status = 10
            return complete_reservation(request, booking)
    else:
        messages.error(request, _('Card can not charged.'))

    return HttpResponseRedirect(reverse('secure_booking'))

@csrf_exempt
def book_place(request):

#    log.info('issecure: %s %s'% (request, request.is_secure()))
    if request.POST.get('placeid'):
        bi = request.POST.copy()
        request.session['booking_selection']=bi
    else:
        bi = request.session.get('booking_selection',{})

    if not request.user.is_authenticated():
        return HttpResponseRedirect('%s?next=%s?express=1'% (reverse('lregister'),reverse('book_place')))

    user = request.user
    place = Place.objects.get(pk=bi['placeid'])
    ci = datetime.strptime(bi['checkin'],'%Y-%m-%d')
    co = datetime.strptime(bi['checkout'],'%Y-%m-%d')
    guests = int(bi['no_of_guests'])
    crrid = bi['currencyid']
    crr,crrposition = Currency.objects.filter(pk=crrid).values_list('name','code_position')[0]
    prices = place.calculateTotalPrice(crrid,ci, co, guests)
#    assert 0,prices

    if bi:
        #FIXME: this is creating lots of stale booking records
        booking = Booking(
            host = place.owner,
            guest = user,
            place = place,
            nights = bi['ndays'],
            guest_payment = prices['total'],
            start = bi['checkin'],
            end = bi['checkout'],
            currency_id =crrid,
            nguests = guests,
        )
        booking.save()
        set_booking(request, booking)

    context ={ 'ci':ci, 'co':co,'ndays':bi['ndays'], 'guests':guests, 'prices': prices,
                  'crr':crr,'crrpos':crrposition,}
    request.session['booking_context'] = context
    context['place']=place
    return HttpResponseRedirect(reverse('secure_booking'))

def process_credit_card(request):
    pos_denizbank = Transaction.get_bank(request)
    booking = get_booking(request)
    data = request.POST
    try:
        exp = data['ccexp'].split('/')
        tl_ucret = booking.currency.convert_to(booking.guest_payment, get_tl_currency_code())
        ccdata={
            'pan' : data['ccno'].replace('-',''),
            'exp_m' : exp[0],
            'exp_y' : exp[1],
            'cv2' : data['ccv'],
            'oid' : booking.id,
            'amount' : tl_ucret,
        }
        odeme_sonucu = pos_denizbank.secure3d_request(ccdata)
        log.info('odeme sonucu : %s' % odeme_sonucu)
#        context['odeme_sonucu'] = odeme_sonucu
    except:
        log.exception('kredi kartiyla odemede hata')
        messages.error(request, _('Error occured.'))
        raise
    return HttpResponse(odeme_sonucu, mimetype='text/html')



def secure_booking(request):
    if request.POST.get('paypal'):
        return HttpResponseRedirect('%s?express=1'%reverse('paypal_checkout'))
    if request.POST.get('banktransfer'):
        return HttpResponseRedirect(reverse('bank_transfer_complete'))
    if request.POST.get('cc'):
        return process_credit_card(request)
    context= request.session.get('booking_context',{})
    booking = get_booking(request)
    context.update({'booking':booking, 'place':booking.place})
    return render_to_response('book_place.html',context, context_instance=RequestContext(request))

def paypal_checkout(request):
#    if request.method == 'POST':
    booking = get_booking(request)
    item = {"PAYMENTREQUEST_0_AMT": str(round(booking.guest_payment,2)),             # amount to charge for item
            'PAYMENTREQUEST_0_DESC':booking.place.title,
            'PAYMENTREQUEST_0_CURRENCYCODE':booking.currency.name,
              "PAYMENTREQUEST_0_INV": "AAAAAA",         # unique tracking variable paypal
              "PAYMENTREQUEST_0_CUSTOM": str(booking.id),       # custom tracking variable for you
              "cancelurl": "%s%s" %(settings.SITE_NAME, reverse('paypal_cancel')),
              "returnurl": "%s%s" %(settings.SITE_NAME, reverse('paypal_checkout')),}

    kw = {"item": item,
        "payment_template": "book_place.html",      #probably not used
        "confirm_template": "paypal-confirm.html",
        "success_url": reverse('paypal_complete'),
        'context':request.session.get('booking_context',{})
    }
    ppp = PayPalPro(**kw)
    return ppp(request)
