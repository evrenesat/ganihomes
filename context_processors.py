__author__ = 'Evren Esat Ozkan'

from website.models.dil import Dil, Ceviriler
from website.models.icerik import Sayfa

__author__ = 'Evren Esat Ozkan'


def website(r):
    soz = {'menu': Sayfa.al_menu(r.LANGUAGE_CODE),
           'diller': Dil.etkin_diller(),
#           'c': Ceviriler.tum_kelimeler(r.LANGUAGE_CODE),
#TODO: tum cevirileri tek bi sozlukten erisilebilir yapmak hos, ama cevir etiketinin islevselligini saglamiyor.
#TODO: dogrusu contexti guncelleyen bir template tag yazmak.

    }
    if r.GET.get('sayfa_id'):
        soz['sayfa_id']= int(r.GET.get('sayfa_id'))
    return soz

