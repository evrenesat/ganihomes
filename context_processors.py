# -*- coding: utf-8 -*-
__author__ = 'Evren Esat Ozkan'

#from website.models.dil import Dil, Ceviriler
#from website.models.icerik import Sayfa
#from places.models import LANG_DROPDOWN

#def website(r):
#    soz = {'menu': Sayfa.al_menu(r.LANGUAGE_CODE),
#           'diller': Dil.etkin_diller(),
##           'c': Ceviriler.tum_kelimeler(r.LANGUAGE_CODE),
##TODO: tum cevirileri tek bi sozlukten erisilebilir yapmak hos, ama cevir etiketinin islevselligini saglamiyor.
##TODO: dogrusu contexti guncelleyen bir template tag yazmak.
#
#    }

from django.conf import settings
def GH(r):
    d = {}
    d['LISTED_LOCALES'] = settings.LISTED_LOCALES
    return d
