# -*- coding: utf-8 -*-
from django.forms.fields import ChoiceField
from website.models.faq import Question
from website.views import addPlaceForm

__author__ = 'Evren Esat Ozkan'

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.utils import simplejson as json
from django.forms.models import ModelForm, ModelChoiceField
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django import http
#from personel.models import Personel, Ileti
#from urun.models import Urun
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_exempt
from places.countries import OFFICIAL_COUNTRIES_DICT, COUNTRIES_DICT
from places.models import Place, Tag, Photo, Currency, Profile, PaymentSelection, SessionalPrice
from django.db import DatabaseError
from places.options import n_tuple, PLACE_TYPES, NO_OF_BEDS
from utils.cache import kes
from website.models.icerik import Sayfa, Haber, Vitrin
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from website.models.medya import Medya
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from  django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer
from django.contrib import auth
from django.contrib import messages
import logging
log = logging.getLogger('genel')



def list_places(request):
    pls = request.user.place_set.all().order_by('-id')
    result = u'[%s]' % u','.join([p for p in pls.values_list('summary', flat=True)])
    return HttpResponse(result, mimetype='application/json')


@csrf_exempt
def save_photo_order(request, id):
    place = get_object_or_404(Place, owner=request.user, pk=id)
    if request.method == 'POST':
        iids = request.POST.get('iids',[])
        place.reorderPhotos(iids)
        return HttpResponse([1], mimetype='application/json')

@csrf_exempt
def save_calendar(request, id):
    place = get_object_or_404(Place, owner=request.user, pk=id)
    if request.method == 'POST':
        unavails = request.POST.get('unavails',[])
#        log.info('unv: %s'%request.POST.get('unavails'))
        place.setUnavailDates(unavails)
        return HttpResponse([1], mimetype='application/json')

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
def dashboard(request):
    rms = request.user.received_messages.all()
    sms = request.user.sent_messages.all()
    context = {'places':request.user.place_set.all(),'form' : addPlaceForm(), 'rms':rms,'sms':sms}
    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))

def show_messages(request, type=None, template='dashboard/user_messages.html'):
    rms = request.user.received_messages.all()
    sms = request.user.sent_messages.all()
    context = {'rms':rms,'sms':sms}
    return render_to_response(template, context, context_instance=RequestContext(request))

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


@login_required
def edit_profile(request):
    lang = request.LANGUAGE_CODE
    user = request.user
    profile = user.get_profile()
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        uform = UserForm(request.POST,instance=user)
        if form.is_valid() and uform.is_valid():
            profile = form.save()
            user = uform.save()
            messages.success(request, _('Your profile successfully updated.'))
    else:
        form = ProfileForm(instance=profile)
        uform = UserForm(instance=user)
    context = {'form':form,'profile':profile,'user':user,'uform':uform}
    return render_to_response('dashboard/edit_profile.html', context, context_instance=RequestContext(request))


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
        fields = ('city','phone','occupation','brithdate')

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
            profile = form.save()
            user = uform.save()
            messages.success(request, _('Your profile successfully updated.'))
    else:
        form = ProfileForm(instance=profile)
        uform = UserForm(instance=user)
    context = {'form':form,'profile':profile,'user':user,'uform':uform}
    return render_to_response('dashboard/edit_profile.html', context, context_instance=RequestContext(request))





@csrf_exempt
def pfoto(request):
    profile = request.user.get_profile()
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'pfoto']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
#        file_size = wrapped_file.file.size
        log.info (u'Got file: %s'%filename)

        profile.photo=file
        profile.save()
        return HttpResponse('[1]', mimetype='application/json')




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
    context = {'bform':bform,'pform':pform, 'ps':ps}
    return render_to_response('dashboard/edit_payment.html', context, context_instance=RequestContext(request))













class PlacePriceForm(ModelForm):
    currency = ModelChoiceField(Currency.objects.filter(active=True), empty_label=None)
    extra_limit = ChoiceField(choices=NO_OF_BEDS)
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
    context = {'bform':form,'sform':spset,}
    return render_to_response('dashboard/edit_prices.html', context, context_instance=RequestContext(request))

