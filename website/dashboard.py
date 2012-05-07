# -*- coding: utf-8 -*-
from django.forms.fields import ChoiceField
from django.utils.html import strip_tags
from support.models import  Ticket, SubjectCategoryTranslation
from website.models.faq import Question
from website.views import addPlaceForm

__author__ = 'Evren Esat Ozkan'

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.forms.models import ModelForm, ModelChoiceField
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from places.models import *
from places.options import   NO_OF_BEDS
from django.http import  HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from datetime import datetime
import logging
log = logging.getLogger('genel')


#TODO: upload donergeci sadece ilk foto icin donuyor
#FIXME: gecici kaydedilen mesajı login sonrası göndermiyor
#FIXME: yorum yaz, duzenle
#FIXME: yorum goster!!!!!!!!!
#FIXME: onaylanmamis mesajlar gonderene gosterilmeli!!

#todo: arkadasliktan cikar




#todo: filebrowser yada ftp
#todo: yorum placeholder
#todo: yorumlu mekan aramada oncelikli


#todo: ganishow alt sekmeleri koyulastir

#todo: ajax history api
#todo: istatisikler
#todo: destek yanit views




def list_places(request):
    pls = request.user.place_set.filter(active=True).order_by('-id')
    return render_to_response('dashboard/place_list.html', {"places":pls}, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def save_photo_order(request, id):
    place = get_object_or_404(Place, owner=request.user, pk=id)
    if request.method == 'POST':
        iids = request.POST.get('iids',[])
        place.reorderPhotos(iids)
        return HttpResponse([1], mimetype='application/json')

@login_required
@csrf_exempt
def add_friend(request, id):
    user = request.user
    requester_profile = user.get_profile()
    other_profile = Profile.objects.get(user_id=id)
    if request.method == 'POST' and not requester_profile.is_friend(other_profile):
        f = Friendship(fr1=requester_profile, fr2=other_profile)
        f.save()
        result = {'message':force_unicode(_('Friendship request successfully sent.'))}
        msg = send_message(request, force_unicode(_('%s wants to be friends with you.')) % user.profile.private_name, receiver=other_profile.user, typ=20)
        msg.status=25
        msg.send_message()
        msg.save()
    else:
        result = {'message':force_unicode(_('Request already exists.'))}
    return HttpResponse(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@login_required
@csrf_exempt
def publish_place(request):
    user = request.user
    if request.method == 'POST':
        id = int(request.POST['id'])
        published = id > 0
        Place.objects.filter(pk=abs(id), owner = user).update(published=published)
        if not published:
            result = {'message':force_unicode(_('Place successfully unlisted from site.'))}
        else:
            result = {'url':reverse('show_place', args=[id]) }
            messages.success(request, _('This place is now published!'))
    return HttpResponse(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@login_required
@csrf_exempt
def delete_place(request):
    user = request.user
    if request.method == 'POST':
        id = int(request.POST['id'])
        Place.objects.filter(pk=id, owner = user).update(active=False, published=False)
        result = {'message':force_unicode(_('Place is deleted.'))}
    return HttpResponse(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@login_required
@csrf_exempt
def confirm_friendship(request):
    user = request.user
    profile = user.get_profile()
    id = int(request.POST.get('id'))
    mid = request.POST.get('mid')
    confirmed =  id>0
    id = abs(id)
    friend = User.objects.get(pk=abs(id))
    if request.method == 'POST':
        f = Friendship.objects.filter(fr2=profile, fr1=friend.get_profile())
        if f:
            f = f[0]
            if confirmed:
                f.confirmed =  True
                f.save()
                result = _('Friendship request accepted.')
            else:
                f.delete()
                result = _('Friendship request declined.')
            send_message(request, force_unicode(result), receiver=friend, replyto=Message.objects.get(pk=mid))
        else:
            result = _('Can\'t find the request. Could be canceled by the other side.')
        result = {'message':force_unicode(result)}
    return HttpResponse(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@csrf_exempt
def save_calendar(request, id):
    place = get_object_or_404(Place, owner=request.user, pk=id)
    if request.method == 'POST':
        unavails = request.POST.get('unavails',[])
#        log.info('unv: %s'%request.POST.get('unavails'))
        place.setUnavailDates(unavails)
        return HttpResponse([1], mimetype='application/json')

@login_required
def calendar(request, id):
    place = get_object_or_404(Place, owner=request.user, pk=id)
    return render_to_response('dashboard/calendar.html',
            {'reserved_dates':place.getReservedDates(), 'place':place},
        context_instance=RequestContext(request))



def show_faq(request, type=None):
    return render_to_response('dashboard/dash_faq.html',
            {'faq':Question.getFaqs(request.LANGUAGE_CODE)},
        context_instance=RequestContext(request))


@login_required
def trips(request):
    user = request.user
    profile = user.get_profile()
    g = user.guestings.filter(status__gt=5)
    context = {
                'current':g.filter(start__lte=datetime.today(), end__gte=datetime.today()),
                'upcoming':g.filter(status__in=[8,9,10,20]),
                'previous':g.filter(end__lte=datetime.today()),
               'bookmarks':profile.favorites.all()
    }
    return render_to_response('dashboard/trips.html', context, context_instance=RequestContext(request))

@login_required
def show_requests(request):
    user = request.user
    profile = user.get_profile()
    context = {
                'requests':user.hostings.filter(status__in=[10,20]),
    }
    return render_to_response('dashboard/requests.html', context, context_instance=RequestContext(request))

@login_required
def show_reviews(request):
    user = request.user
    profile = user.get_profile()
    byyou = list(user.place_reviews_by_you.all()) + list(user.personal_reviews_by_you.all())
    aboutyou = list(user.place_reviews_about_you.all()) + list(user.personal_reviews_about_you.all())
    context = {
                'byyou':byyou,
                'aboutyou':aboutyou,
    }
    return render_to_response('dashboard/reviews.html', context, context_instance=RequestContext(request))

@login_required
def friends(request):
    user = request.user
    profile = user.get_profile()
    context = {
               'friends' : profile.get_friends()
    }
    return render_to_response('dashboard/friends.html', context, context_instance=RequestContext(request))

def list_messages(rq, count=None):
    user = rq.user
    msgs = []
    anamesajlar = set()

    mesajlar = Message.objects.select_related().filter( receiver=user, read=False, status__in=[20,25]).order_by('-id','-last_message_time')
    if mesajlar:
        if count: mesajlar = mesajlar[:count]
        for m in mesajlar:
            anamesajlar.add(m.replyto if m.replyto else m)
    if count and len(anamesajlar) < count or not anamesajlar :
        mesajlar = Message.objects.select_related().filter( Q(sender=user)|Q(receiver=user), replyto__isnull=True,  status__in=[20,25]).order_by('-last_message_time')
        if mesajlar:
            if count: mesajlar = mesajlar[:count]
            for m in mesajlar:
                anamesajlar.add(m.replyto if m.replyto else m)



    for m in anamesajlar:
        m.icon = 'read'
        m.line = m.get_type_display()
        if m.sender != user:
            m.participant = m.get_sender_name()
            if not m.read:
                m.icon = 'new'
        else:
            if m.type==20:
                m.line = force_unicode(_('Friend request to %s'))
            m.participant = m.get_receiver_name()

        if m.type in [10,20]:
            obj = m.participant
        elif m.type == 30:
            obj = m.place.title
        else:
            obj = None

        if obj:
            m.line = m.line % obj

        if m.replied:
            latest  = m.message_set.latest()
            if not latest.read and latest.sender!=user:
                m.icon = 'replied'
        msgs.append(m)
    return msgs

@login_required
def dashboard(request):
    user = request.user
    profile = user.get_profile()
    bookings = []
    bookings.extend(Booking.objects.filter(status__in=[10,20,30], valid=True, host=user)[:4])
    bookings.extend(Booking.objects.filter(status__in=[8,9,10,20,30], valid=True, guest=user)[:4])
    context = {'places':user.place_set.all(),
               'form' : addPlaceForm(),
               'msgs':list_messages(request, 4),
               'bookmarks':profile.favorites.all(),
               'bookings':bookings,

    }
    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))

@login_required
def show_messages(request):
    context = {'msgs':list_messages(request),}
    return render_to_response('dashboard/user_messages.html', context, context_instance=RequestContext(request))


class PlaceReviewForm(ModelForm):
    class Meta:
        model = PlaceReview
        fields = ('text','location_rating','comfort_rating','clean_rating','value_money_rating','overall_rating')
        #exclude = ('',)


@login_required
def review_place(request, id):
    user = request.user
    b = Booking.objects.get(Q(guest=user)|Q(host=user), pk=id)
    if request.method == 'POST':
        form = PlaceReviewForm(request.POST)
        r=form.save(commit=False)
        r.writer = user
        r.booking = b
        r.person = b.owner
    else:
        form = PlaceReviewForm()
    context={
        'user_is_guest':b.guest == user,
        'user_is_host':b.host == user,
        'total_price': b.guest_payment,
        'booking':b,
        'place':b.place,
    }

    return render_to_response('dashboard/review_place.html', context, context_instance=RequestContext(request))

@login_required
def show_booking(request, id):
    user = request.user
    b = Booking.objects.get(Q(guest=user)|Q(host=user), pk=id)
    if request.method =='POST':
        #FIXME: durum degisikliginden misafiri/ev sahibini haberdar etmek gerek
        admin_warn='Tanimsiz rezervasyon islemi'
        job = request.POST.get('confirmation')
#        assert 0, user.id
        if user == b.guest:

            if job == 'cancel' and b.status<=10:
                b.status = 50
                b.rejection_date = datetime.now()
                b.voidPayment(request)
                b.del_reservation()
                messages.info(request, _('Booking request canceled.'))
                admin_warn='Rezervasyon istegi misafir tarafindan iptal edildi.'
            if job == 'banktransfer' and b.status==8:
                b.status = 9
                b.payment_notification_date = datetime.now()
                b.rejection_date = datetime.now()
                messages.info(request, _('Thank you. Your booking request will be processed after your payment reviewed by our staff.'))
                admin_warn='Rezervasyon odemesi yapıldı!!!'
            elif job =='confirmpayment'  and b.status==20:
                b.status = 30
                b.guest_ok_date = datetime.now()
                messages.success(request, _('Accommodation confirmed.'))
                admin_warn='Konaklama misafir tarfindan onaylandi. Ucret aktarimi gerekli!!!'
        elif user == b.host and b.status<=10:
            if job =='confirm':
                b.status = 20
                b.confirmation_date = datetime.now()
                b.capturePayment(request)
                messages.success(request, _('Booking request confirmed.'))
                admin_warn='Rezervasyon istegi ev sahibi tarafindan onaylandi.'
            elif job =='reject':
                b.status = 40
                b.rejection_date = datetime.now()
                b.voidPayment(request)
                messages.info(request, _('Booking request rejected.'))
                admin_warn='Rezervasyon istegi ev sahibi tarafindan reddedildi.'
        b.save()
        mail2perm(b, url=reverse('admin:places_booking_change', args=(b.id, )), pre=admin_warn, sbj=u'Rezervasyon güncellemesi')
    context={
        'user_is_guest':b.guest == user,
        'user_is_host':b.host == user,
        'total_price': b.guest_payment,
        'booking':b,
        'place':b.place,
        'voidable_status_codes': (8, 9, 10),
        'status' : BOOKING_STATUS_FOR_GUEST[b.status] if b.guest == user
              else BOOKING_STATUS_FOR_HOST[b.status]
    }
        #todo: send_message to guest
    return render_to_response('dashboard/show_booking.html', context, context_instance=RequestContext(request))


@login_required
def show_message(request, id):
    user = request.user
    profile = user.get_profile()
    msg = Message.objects.get(Q(sender=user)|Q(receiver=user), pk=id)
    msg.message_set.filter(read=False, receiver=user).update(read=True)
    if msg.receiver == user:
        participant = msg.sender
        receiver = msg.sender
        if not msg.read:
            msg.read = True
            msg.save()
    else:
        participant = msg.receiver
        receiver = msg.receiver
    participant_profile = participant.get_profile()
    if request.method == 'POST':
        send_message(request, strip_tags(request.POST['message']), receiver=receiver, replyto=msg)
        msg.last_message_time = datetime.now()
        msg.replied = True
        msg.save()
        messages.success(request, _('Your message successfully sent.'))

    msgs = list(Message.objects.select_related().filter(replyto=msg))
    msgs.append(msg)
    msgslist = []
    for m in msgs:
        m.sender_name =  m.sender.get_full_name() if m.sender == user else m.get_sender_name()
        msgslist.append(m)
    context = {'msg':msg,
               'msgs':msgslist,
               'participant':participant,
               'toname':participant.get_profile().private_name,
               'friends':profile.is_friend(participant_profile),
    }
    return render_to_response('dashboard/show_message.html', context, context_instance=RequestContext(request))

#@csrf_exempt
@login_required
def new_message(request, id):
    user = request.user
    receiver = User.objects.get(pk=id)
    profile = user.get_profile()
    receiver_profile = receiver.get_profile()
    if request.method == 'POST':
        msg = send_message(request, strip_tags(request.POST['message']), receiver=receiver)
        messages.success(request, _('Your message successfully sent.'))
        return HttpResponseRedirect(reverse('show_message', args=[msg.id]))
    context = {'participant':receiver,
               'toname':receiver_profile.private_name,
               'friends':profile.is_friend(receiver_profile),
    }
    return render_to_response('dashboard/show_message.html', context, context_instance=RequestContext(request))

class PasswordForm(forms.Form):
    old = forms.CharField(widget=forms.PasswordInput(),label=_('Old password'))
    new1 = forms.CharField(widget=forms.PasswordInput(),label=_('New password'))
    new2 = forms.CharField(widget=forms.PasswordInput(),label=_('New password (again)'))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old']):
                if form.cleaned_data['new1']==form.cleaned_data['new2']:
                    user.set_password(form.cleaned_data['new1'])
                    messages.success(request, _('Your password successfully changed.'))
                else:
                    messages.error(request, _('The two password fields didn\'t match.'))
            else:
                messages.error(request, _('Your old password was entered incorrectly. Please enter it again.'))
    else:
        form = PasswordForm()
    context = {'form':form,}
    return render_to_response('dashboard/change_password.html', context, context_instance=RequestContext(request))

class ProfileForm(ModelForm):
#    lat= forms.FloatField(widget=forms.HiddenInput())
#    lon= forms.FloatField(widget=forms.HiddenInput())
#    currency = ModelChoiceField(Currency.objects.filter(active=True), empty_label=None)

#    neighborhood= forms.FloatField(widget=forms.HiddenInput())

#    postcode= forms.CharField(widget=forms.HiddenInput())
#    def __init__(self, *args, **kwargs):
#        super(ProfileForm, self).__init__(*args, **kwargs)
#        self.fields.insert (0, 'first_name' , forms.CharField())
#        self.fields.insert (1, 'last_name' , forms.CharField())
#        self.fields.insert (2, 'email' , forms.EmailField())

    class Meta:
        model=Profile
        fields = ('city','phone','occupation','brithdate','bio')

class UserForm(ModelForm):
    class Meta:
        model=User
        fields = ('first_name','last_name','email')

@login_required
def edit_profile(request):
    lang = request.LANGUAGE_CODE
    user = request.user
    profile = user.get_profile()
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        uform = UserForm(request.POST,instance=user)
        if form.is_valid() and uform.is_valid():
            if User.objects.filter(username=uform.cleaned_data['email']).exclude(id=user.id):
                messages.error(request, _('This email address is already in use.'))
            else:
                profile = form.save()
                user = uform.save(commit=False)
                user.username = user.email
                user.save()
                messages.success(request, _('Your profile successfully updated.'))
    else:
        form = ProfileForm(instance=profile)
        uform = UserForm(instance=user)
    context = {'form':form,'profile':profile,
               'user':user,'uform':uform,
    }
    return render_to_response('dashboard/edit_profile.html', context, context_instance=RequestContext(request))




@login_required
@csrf_exempt
def pfoto(request):
    profile = request.user.get_profile()
    if request.method == 'POST':
#        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'pfoto']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
#        file_size = wrapped_file.file.size
#        log.info (u'Got file: %s'%filename)

        profile.photo=file
        profile.save()
        return HttpResponse('[1]', mimetype='text/html')




class PaymentSelectionBankForm(ModelForm):
    class Meta:
        model=PaymentSelection
        exclude= ('email','user','payment_type','active')
class PaymentSelectionPaypalForm(ModelForm):
    class Meta:
        model=PaymentSelection
        fields= ('email',)

@login_required
def edit_payment(request):
    user = request.user
    ps,yeni=PaymentSelection.objects.get_or_create(user=user)
    saved_ps = None
    if request.method == 'POST':
        bform = PaymentSelectionBankForm(request.POST,instance=ps)
        pform = PaymentSelectionPaypalForm(request.POST,instance=ps)
        if bform.is_valid():
            saved_ps = bform.save(commit=False)
            saved_ps.payment_type =3 #bank transfer
        if pform.is_valid():
            saved_ps = pform.save(commit=False)
            saved_ps.payment_type = 2 #paypal
        if saved_ps:
            saved_ps.save()
            messages.success(request, _('Your payment selection successfully updated.'))
    else:
        bform = PaymentSelectionBankForm(instance=ps)
        pform = PaymentSelectionPaypalForm(instance=ps)

    context = {'bform':bform,'pform':pform, 'ps':ps,
               'iban_countries':json.dumps(configuration('iban_countries').upper().split(','), ensure_ascii=False)
    }
    return render_to_response('dashboard/edit_payment.html', context, context_instance=RequestContext(request))













class PlacePriceForm(ModelForm):
    currency = ModelChoiceField(Currency.objects.filter(active=True), empty_label=None, label=_('Currency'))
    extra_limit = ChoiceField(choices=NO_OF_BEDS,label=_('Extra charge for more guests than'))
    class Meta:
        model=Place
        fields = ('price','currency','weekend_price','weekly_discount','monthly_discount','extra_limit','extra_price','cleaning_fee')

from django.forms.models import modelformset_factory
SPFormSet = modelformset_factory(SessionalPrice, extra=2,  exclude=('place','active'),can_delete =True)

@login_required
def edit_prices(request, id):
    lang = request.LANGUAGE_CODE
    user = request.user
    place = Place.objects.get(pk=id, owner=user)
    if request.method == 'POST':
        form = PlacePriceForm(request.POST,instance=place)
        spset = SPFormSet(request.POST, queryset=SessionalPrice.objects.filter(place=place))

        if spset.is_valid():
            spset = spset.save(commit=False)
            for f in spset:
                f.place = place
                f.save()
        if form.is_valid():
            saved_place = form.save()

            messages.success(request, _('Your pricing successfully updated.'))

    form = PlacePriceForm(instance=place)
    spset = SPFormSet(queryset=SessionalPrice.objects.filter(place=place))
    context = {'bform':form,'sform':spset,'place':place, 'host_fee':configuration('host_fee'), }
    return render_to_response('dashboard/edit_prices.html', context, context_instance=RequestContext(request))



class TicketForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': '30', 'rows': '4'}), label=_(u'Your message'))
    subject = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}), label=_(u'Subject'))
    #    tip = forms.ChoiceField(label='Değerlendirme',  choices=Mesaj.TIP)
#    category = forms.ModelChoiceField(queryset=SubjectCategory.objects.exclude(hidden=True), label=_(u'Category'))

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang')
        super(TicketForm, self).__init__(*args, **kwargs)
#        self.fields['tags'].widget = forms.CheckboxSelectMultiple()
        self.fields["category"].choices = [(c.category_id, c.text) for c in SubjectCategoryTranslation.objects.filter(lang=lang)]
#        self.fields['currency'].queryset = Currency.objects.filter(active=True)

    class Meta:
        model = Ticket
        exclude = ('user', 'status')


@login_required
def support_create(request):
    if request.POST:
        form = TicketForm(request.POST, lang=request.LANGUAGE_CODE)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 10
            obj.user = request.user
            obj.save()
            mail2perm(obj, url=reverse('support_admin_show_ticket', args=(obj.id, )))
            messages.success(request, _('Your message successfully saved.'))
#            return HttpResponseRedirect(reverse('support_thanks'))
    else:
        form = TicketForm(lang=request.LANGUAGE_CODE)
        form.fields['subject'].initial = request.GET.get('subject', '')
        form.fields['category'].initial = int(request.GET.get('category', 0))
    return render_to_response('dashboard/support_create.html', {'form': form, },
                              context_instance=RequestContext(request, {}))



class InviteForm(forms.Form):
    name = forms.CharField(label=_('Name of your friend'))
    email = forms.CharField(label=_('Email of your friend'))
    note = forms.CharField(label=_('Optional note to your friend'), widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), required=False)


@login_required
def invite_friend(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            user = request.user
            messages.success(request, _('Invite message successfully sent.'))
            sender_name = user.get_full_name()
            subject = force_unicode(_('%s has invited you to GaniHomes'))% sender_name
            name = form.cleaned_data['name']
            msg_context ={'name':name,
                          'note':form.cleaned_data['note'],
                          'sender':sender_name,
                          'LANGUAGE_CODE':request.LANGUAGE_CODE}
            send_html_mail(subject,
                form.cleaned_data['email'],
                msg_context,
                template='mail/invite_message.html',
                recipient_name=name)
        else:
            messages.error(request, _('Form has errors, please check your input.'))
    else:
        form = InviteForm()
    context = {'form':form,}
    return render_to_response('dashboard/invite_friend.html', context, context_instance=RequestContext(request))


@login_required
def edit_description(request,pid):
    place = Place.objects.get(pk=pid, owner=request.user)
    default_lang = place.lang or request.LANGUAGE_CODE
    tlangs = configuration('trans_langs').replace(' ','').split(',')
    if request.method == 'POST':
        p = request.POST.copy()
        for lang in tlangs:
            desc = p.get('des_%s'%lang)
            if desc:
                title = p.get('tit_%s'%lang)
                d, new = Description.objects.get_or_create(place=place, lang=lang)
                d.text = desc
                d.title = title
                d.save()
                if lang == default_lang:
                    place.description = desc
                    place.title = title
                    place.translated = False
                    place.save()
            else:
                Description.objects.filter(place=place, lang=lang).delete()
        messages.success(request, _('Your translations successfully saved.'))
    langs = []
    descs={}
    for d in Description.objects.filter(place=place):
        descs[d.lang]=d
    for l in tlangs:
        lan = [l, LANG_DICT[l]]
        if descs.get(l):
            lan.extend([descs[l].title,  descs[l].text,  descs[l].auto ])
        langs.append(lan)
    context = {'langs':langs}
    return render_to_response('dashboard/edit_description.html', context, context_instance=RequestContext(request))

