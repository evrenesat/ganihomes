from django.templatetags.static import register
from website.models.dil import Ceviriler

__author__ = 'Evren Esat Ozkan'

def cevir(context, kelime):
    return Ceviriler.cevir(kelime,context['LANGUAGE_CODE'])

def urlcevir(context, url):
    return ('%s/%s' % (context['LANGUAGE_CODE'],url)).replace('//','/')

register.simple_tag(takes_context=True)(cevir)
register.simple_tag(takes_context=True)(urlcevir)
