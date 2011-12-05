# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils import simplejson as json
from django.forms.models import ModelForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django import http
#from personel.models import Personel, Ileti
#from urun.models import Urun
from django.views.decorators.csrf import csrf_exempt
from places.models import Place, Tag, Photo
from django.db import models
from places.options import n_tuple, PLACE_TYPES
from website.models.icerik import Sayfa, Haber, Vitrin
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from website.models.medya import Medya
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from  django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
import logging
log = logging.getLogger('genel')
noOfBeds=n_tuple(7, first=[(0,u'--')])
placeTypes = [(0,_(u'All'))] + PLACE_TYPES

class SearchForm(forms.Form):
    checkin = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    checkout = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    search_pharse = forms.CharField(widget=forms.TextInput())
    no_of_guests = forms.ChoiceField(choices=noOfBeds, initial=1, label=_(u'Guests'))
    placeType = forms.ChoiceField(choices=placeTypes)

class BookingForm(forms.Form):
    checkin = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    checkout = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    no_of_guests = forms.ChoiceField(choices=noOfBeds, initial=1)


def showPlace(request, id):
    place = Place.objects.get(pk=id)

    context = {'place':place,'bform':BookingForm() }
    return render_to_response('show_place.html', context, context_instance=RequestContext(request))

def searchPlace(request):
    context = {}
    return render_to_response('search_place.html', context, context_instance=RequestContext(request))

class LoginForm(forms.Form):
    login_email = forms.EmailField(label=_(u'E-mail address'))
    login_pass = forms.CharField(widget=forms.PasswordInput(),label=_(u'Password'))

class RegisterForm(ModelForm):
    pass1 = forms.CharField(widget=forms.PasswordInput(),label=_(u'Password'))
    pass2 = forms.CharField(widget=forms.PasswordInput(),label=_(u'Password (Again)'))
    email = forms.EmailField(label=_(u'E-mail address'))
    class Meta:
        model=User
        fields = ('email','first_name','last_name',)

def anasayfa(request):
    sayfa = Sayfa.al_anasayfa()
    lang = request.LANGUAGE_CODE
    searchForm = SearchForm()
    context = {'slides': Vitrin.get_slides(), 'slides2': Vitrin.get_slides(type=1),
               'slides3': Vitrin.get_slides(type=2), 'srForm':searchForm }
    return render_to_response('index.html', context, context_instance=RequestContext(request))

class addPlaceForm(ModelForm):
    geocode= forms.CharField(widget=forms.HiddenInput())
    postcode= forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        super(addPlaceForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()

    class Meta:
        model=Place
        fields = ('title','type','capacity','space','description','price','currency',
            'city','country','district','street','address','geocode',
            'postcode','tags', 'min_stay', 'max_stay', 'cancellation','manual','rules'
            )

def addPlace(request, template_name="add_place.html", id=None):
    sayfa = Sayfa.al_anasayfa()
    lang = request.LANGUAGE_CODE
    user = request.user
    loged_in = user.is_authenticated()
    if id:
        old_place = get_object_or_404(Place, pk=id)
        if old_place.owner != request.user:
            raise HttpResponseForbidden()
    else:
        old_place = Place()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        login_form = LoginForm(request.POST)
        form = addPlaceForm(request.POST, instance=old_place)
        if form.is_valid():
            new_place=form.save(commit=False)
            if register_form.is_valid() or loged_in:
                if not loged_in:
                    user = register_form.save(commit=False)
                    user.username = user.email
                    user.save()
                new_place.owner = user
                new_place.save()
                form.save_m2m()
                for tag in form.cleaned_data['tags']:
                    new_place.tags.add(tag)
                new_place.save()
                tmp_photos = request.session.get('tmp_photos')
                if tmp_photos:
                    Photo.objects.filter(id__in=tmp_photos).update(place=new_place)
                return HttpResponseRedirect(reverse('show_place', args=[new_place.id]))
    else:
        form = addPlaceForm(instance=old_place)
        register_form = RegisterForm()
        login_form = LoginForm()
    context = {'form':form, 'rform':register_form,'lform':login_form,'place':old_place}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


#def bannerxml(request, tip):
#    lang = request.LANGUAGE_CODE
#    context = {'slides': Vitrin.al_slide(banner_tip=tip, dilkodu=lang), }
#    ci = RequestContext(request)
#    return render_to_response('banner.xml', context, context_instance=ci)

#
#class IletisimForm(ModelForm):
#    class Meta:
#        model = Ileti
#        fields = ('gonderen_ad', 'gonderen_eposta', 'konu', 'yazi')
#
#
#def iletisim(request, urun_id=None):
#    lang = request.LANGUAGE_CODE
#    ilgili_urun_id = request.REQUEST.get('ilgili_urun')
#
##    urun = Urun.objects.get(pk=urun_id) if urun_id else None
#    urun = None
#    if request.method == 'POST':
#        form = IletisimForm(request.POST)
#        if form.is_valid():
#            i = form.save(commit=False)
#            i.ip = request.META.get('REMOTE_ADDR')
#
#            if urun:
#                tesk_msj='Ürünümüz hakkındaki mesajınız alındı. Teşekkür Ederiz.'
#                i.yazi = '%s adlı ürün hakkında;\n\n%s' % (urun.baslik(), i.yazi)
#            else:
#                tesk_msj='Mesajınız alındı. Teşekkür Ederiz.'
#            i.save()
#            messages.add_message(request, messages.INFO, tesk_msj)
#            return HttpResponseRedirect('/%s/mesaj_goster/'%lang)
#    else:
#        form = IletisimForm()
#        if urun:
#            form.fields['konu'].initial = urun.al_baslik(lang)
#    context = {'form': form,}
#    if urun:
#        context.update({'urun':urun,'icerik':urun.al_icerik(lang),
#                'kategoriler': urun.kategoriler(lang)})
#    elif request.GET.get('sayfa_id'):
#        context.update({'kategoriler':Sayfa.objects.get(pk=int(request.GET.get('sayfa_id'))).kategoriler(lang) })
#
#    ci = RequestContext(request)
#    return render_to_response('iletisim.html', context, context_instance=ci)


def icerik(request, id, slug):
    sayfa = get_object_or_404(Sayfa, pk=id)
    lang = request.LANGUAGE_CODE
    context = {'sayfa_id': sayfa.id, 'sayfa': sayfa,
               'icerik': sayfa.al_icerik(lang),
               'kategoriler': sayfa.kategoriler(lang)}
    ci = RequestContext(request)
    sablon = sayfa.sablon or 'icerik.html'
    return render_to_response(sablon, context, context_instance=ci)


def mesaj_goster(request):
    lang = request.LANGUAGE_CODE
    sayfa = Sayfa.al_anasayfa()
    context = {'sayfa': sayfa,'kategoriler': sayfa.kategoriler(lang)}
    ci = RequestContext(request)
    return render_to_response('content.html', context, context_instance=ci)


def haber_goster(request, id, slug):
    haber = get_object_or_404(Haber, pk=id)
    lang = request.LANGUAGE_CODE
    context = {'sayfa_id': haber.id, 'sayfa': haber,
               'icerik': {'metin': haber.icerik, 'baslik': haber.baslik},
               'kategoriler': haber.kategoriler(request.LANGUAGE_CODE)}
    ci = RequestContext(request)
    return render_to_response('content.html', context, context_instance=ci)


def dilsec(request, kod):
    url = request.GET.get('url')
    url = '/%s%s/' % (kod[:2], url[3:] if url else '/')
    return HttpResponseRedirect(url.replace('//', '/'))



@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. Photo id='+str(pk))
        image = get_object_or_404(Photo, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Recieved not POST request todelete image view')
        return HttpResponseBadRequest('Only POST accepted')



def square_thumbnail(source):
    thumbnail_options = dict(size=(50, 50), crop=True)
    return get_thumbnailer(source).get_thumbnail(thumbnail_options)

@csrf_exempt
def multiuploader(request):
    #FIXME : file type checking
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "'+str(filename)+'"')

        #writing file manually into model
        #because we don't need form of any type.
        image = Photo()
        image.name=str(filename)
        image.image=file
        image.save()
        tmp_photos = request.session.get('tmp_photos',[])
        tmp_photos.append(image.id)
        request.session['tmp_photos'] = tmp_photos
        log.info('File saving done')

        #getting url for photo deletion
        file_delete_url = '/delete/'

        #getting file url here
        file_url = image.image.url

        #getting thumbnail url using sorl-thumbnail
        im = square_thumbnail(image.image)
        thumb_url = im.url
#        thumb_tag = im.tag()

        #generating json response array
        result = []
        result.append({"name":filename,
                       "size":file_size,
                       "url":file_url,
#                       "tag":thumb_tag,
                       "turl":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/',
                       "delete_type":"POST",})
        response_data = json.dumps(result)
        return HttpResponse(response_data, mimetype='application/json')


def image_view(request):
    items = Photo.objects.all()
    return render_to_response('images.html', {'items':items})

def statusCheck(request):
    context={
        'authenticated':request.user.is_authenticated(),
    }
    response =  HttpResponse(json.dumps(context), mimetype='application/json')
    response.set_cookie('lin', 1 if context['authenticated'] else -1)
    return response


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        rform = RegisterForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login_email'], password=form.cleaned_data['login_pass'])
            if user:
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                auth_login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.error(request, _('Wrong email or password.'))
    else:
        form = LoginForm()
        rform = RegisterForm()
    context = {'form':form, 'rform':rform}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

def register(request):
    sayfa = Sayfa.al_anasayfa()
    lang = request.LANGUAGE_CODE
    user = request.user
    loged_in = user.is_authenticated()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['pass1']==form.cleaned_data['pass2']:
                user = form.save(commit=False)
                user.username = user.email
                user.set_password(form.cleaned_data['pass1'])
                user.save()
                return HttpResponseRedirect(reverse('registeration_thanks'))
            else:
                messages.error(request, _('The passwords you entered do not match.'))
    else:
        form = RegisterForm()
    context = {'form':form}
    return render_to_response('register.html', context, context_instance=RequestContext(request))


def dashboard(request):
    context = {'places':request.user.place_set.all(),'form' : addPlaceForm()}
    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))

def registeration_thanks(request):
    context = {}
    return render_to_response('registeration_thanks.html', context, context_instance=RequestContext(request))
