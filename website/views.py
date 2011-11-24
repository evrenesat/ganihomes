# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import ModelForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django import http
#from personel.models import Personel, Ileti
#from urun.models import Urun
from places.models import Place
from places.options import n_tuple, PLACE_TYPES
from website.models.icerik import Sayfa, Haber, Vitrin
from django.http import HttpResponseRedirect
from website.models.medya import Medya
from django.contrib import messages

class SearchForm(forms.Form):
    noOfBeds=n_tuple(7, first=[(0,u'--')])
    placeTypes = [(0,u'--')] + PLACE_TYPES
    checkin = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    checkout = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    search_pharse = forms.CharField(widget=forms.TextInput())
    no_of_guests = forms.ChoiceField(choices=noOfBeds, initial=1)
    placeType = forms.ChoiceField(choices=placeTypes)


def anasayfa(request):
    sayfa = Sayfa.al_anasayfa()
    lang = request.LANGUAGE_CODE
    searchForm = SearchForm()
    context = {'slides': Vitrin.get_slides(), 'slides2': Vitrin.get_slides(type=1),
               'slides3': Vitrin.get_slides(type=2), 'srForm':searchForm }
    return render_to_response('index.html', context, context_instance=RequestContext(request))

class addPlaceForm(ModelForm):
    class Meta:
        model=Place
        fields = ('title','type','capacity','space','bedroom','description','price','currency',)

def addPlace(request):
    sayfa = Sayfa.al_anasayfa()
    lang = request.LANGUAGE_CODE
    if request.method == 'POST':
        form = addPlaceForm(request.POST)

    else:
        form = addPlaceForm()
    context = {'form':form}
    return render_to_response('mekan_ekle.html', context, context_instance=RequestContext(request))


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

