from django.templatetags.static import register
from website.models.dil import __


__author__ = 'Evren Esat Ozkan'

def cevir(kelime):
    return __(kelime)


def urlcevir(context, url):
    return ('%s/%s' % (context['LANGUAGE_CODE'],url)).replace('//','/')

register.simple_tag()(cevir)
register.simple_tag(takes_context=True)(urlcevir)
