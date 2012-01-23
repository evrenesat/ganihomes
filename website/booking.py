# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_exempt
from paypal.pro.models import PayPalNVP
from places.models import Place, Currency, Booking
from django.http import HttpResponseRedirect
from  django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import logging
from website.views import send_message

log = logging.getLogger('genel')
from datetime import datetime
from paypal.pro.views import PayPalPro
from appsettings import app
ghs = app.settings.gh


def get_booking(rq):
    return Booking.objects.get(pk=rq.session['booking_id']) if rq.session.get('booking_id') else False

def set_booking(rq, bk):
    rq.session['booking_id'] = bk.id

def paypal_complete(request):
    booking = get_booking(request)
    paypal_transaction = PayPalNVP.objects.get(method="DoExpressCheckoutPayment",ack='Success',custom=str(booking.id))
    booking.payment_type = 2
    booking.status = 10
    booking.save()

    msg = _("""%(guest)s would like to stay at your place %(title)s on %(start)s through %(end)s. Please <a href='?showBookingRequest=%(bid)s'>accept or decline</a> this  reservation in 24 hours .
    Phone, email, and address information will be exchanged between guest/host after you accept the guest.
    """)
    msg = force_unicode(msg) % {
        'guest':booking.guest.get_profile().private_name,
        'title':booking.place.title,
        'start':booking.start,
        'end':booking.end,
        'bid':booking.id,
    }
    send_message(request, msg, place=booking.place, typ=30)
    messages.success(request, _('Your booking request has been successfully sent to the host.'))
    return HttpResponseRedirect(reverse('dashboard'))

def paypal_cancel(request):
    return render_to_response('paypal-cancel.html',{}, context_instance=RequestContext(request))

@csrf_exempt
def book_place(request):

    log.info('issecure: %s %s'% (request, request.is_secure()))
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
    guests = bi['no_of_guests']
    crrid = bi['currencyid']
    crr,crrposition = Currency.objects.filter(pk=crrid).values_list('name','code_position')[0]
    prices = place.calculateTotalPrice(crrid,ci, co, guests)

    if request.method == 'POST':
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
        booking.set_reservation()
        booking.save()
        set_booking(request, booking)
        if request.POST.get('paypal'):
            return HttpResponseRedirect('%s?express=1'%reverse('paypal_checkout'))

    context ={ 'ci':ci, 'co':co,'ndays':bi['ndays'], 'guests':guests, 'prices': prices,
                  'crr':crr,'crrpos':crrposition,}
    request.session['booking_context'] = context
    context['place']=place
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
