#! /usr/bin/env python
# -*-  coding: utf-8 -*-
import sys
import os
from apiclient.http import HttpRequest

pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.abspath(pathname))
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from applicationinstance import ApplicationInstance

from apiclient.discovery import build
from places.models import Place, Description
#from utils.cache import kes

DEVELOPER_KEY = 'AIzaSyAd8evO6SwmuE3RoBdaROzLoNGesc386Vg'

import logging
log = logging.getLogger('genel')
import httplib2
httplib2.debuglevel = 4

from configuration import configuration

class HttpPostRequest(HttpRequest):
    def __init__(self, *args, **kwargs):
        kwargs['method']='POST'
        kwargs['headers']={
            'X-HTTP-Method-Override':'GET',
#            'Content-Length':'81',
                           }
        HttpRequest.__init__(self, *args, **kwargs)

class TranslationMachine:
    """
    google translation machine
    """
    def __init__(self):
        self.auto_langs = configuration('auto_trans_langs').split(',')
        self.service = build('translate', 'v2', developerKey=DEVELOPER_KEY)
        self.pservice = build('translate', 'v2', developerKey=DEVELOPER_KEY, requestBuilder=HttpPostRequest)#
        self.run()

    def translate(self, input, target, source=None):
        try:
#            print target,input
            if source:
                tr = self.service.translations().list(source=source, target=target, q=input).execute()
            else:
                tr = self.pservice.translations().list(target=target, q=input).execute()
            return   tr['translations']
        except:
#            log.exception('unexpected error')
            pass

    def run(self):
#        print self.auto_langs

        for p in Place.objects.filter(translation_status__lt=30):
            if len(p.description)<8:
                log.info('%s aciklamasi fazla kisa, pass' % p)
                continue
            already_translated_langs = p.get_translation_list(reset=True)
            for l in self.auto_langs:
                if l not in already_translated_langs:

                    translation = self.translate([p.title,p.description],l)
                    print 'TRANSLATION RESULT FOR %s %s' % (p.id, p.title), translation
                    if translation:
#                        print 'laaaaaaaaaaaaaaan',p.title,l
#                        print translation[0]
                        d, new = Description.objects.get_or_create(place=p, lang=l)
                        d.text = translation[1]['translatedText']
                        d.title = translation[0]['translatedText']
                        d.auto = True
                        d.save()
            translated_langs = p.get_translation_list(reset=True)
            if translated_langs:
                p.translation_status = 20
                if all([ l in translated_langs for l in self.auto_langs ] ):
                    p.translation_status = 30
                p.save()














#
#
#if __name__ == '__main__':
#    o = None
#    inst = None
#    try:
#        inst = ApplicationInstance( '/tmp/gtranslate.pid' )
#
#        o = TranslationMachine()
#        if inst:
#            inst.exitApplication()
#    except SystemExit:
#        if inst:
#            inst.exitApplication()
#        pass
#    except:
#        if inst:
#            inst.exitApplication()
#        log.exception('beklenmeyen hata')
#
text='''
YES, This is a real and direct view right from the apartment windows!

Prices are good through 2011.

- Furnished and beautiful one bedroom Apartment
- On the Seine river (on the Quai)
- Direct, unobstructed view of the Eiffel Tower and the Seine
- Best view ever
- Bright & Sunny
- Very romantic location
- At the bottom of the Trocadero
- Walking distance to many Museums - Palais de Tokyo - The Paris Modern Art Museum - Marmottan & Claude Monet Museum - Quai Branly Museum - Galleria (list is too long)
- Walking distance to many restaurants (Including Philip Starck's Le Bon etc.)
- Great location close to the Champs Elysees, Concorde
- Bathroom with tub
- Free Internet / Wifi
- harman kardon speakers to be connected directly to your IPOD or computer for background music.

Kitchen:
- Fully equipped with all your needs.

Location:
- Accessible to all kinds of transportation: Bus, Metro, Velib
- Plenty of street parking for your rental.
- Post office at the bottom of the building
- All your needs and convenience stores and shopping on rue de passy

Accessibility:
Metro Passy - Line 6 or Metro Trocadero - Line 6 or 9
RER C - Champs de Mars-Tour Eiffel

Station Passy (196m/214 yards) - Métro ligne 6
1 Rue de Passy, 75016, Paris
Station Trocadéro (462m/505 yards) - Métro lignes 6, 9
Musée national de la Marine, 17 place du Trocadéro, 75116, Paris
Station Bir Hakeim-Champ de Mars-Tour Eiffel (500m/550 yards) - Métro ligne 6
105 Quai Branly, 75015, Paris
Station Iéna (637m/700 yards) - Métro ligne 9
1 Avenue d'Iéna, 75116, Paris
Station Bir Hakeim-Champ de Mars-Tour Eiffel (500m/ 550 yards) - RER ligne C
105 Quai Branly, 75015, Paris'''



import urllib
import urllib2

url = 'https://www.googleapis.com/language/translate/v2'

values = {'key' : DEVELOPER_KEY,
          'target' : 'tr',
          'q' : text }
headers={'X-HTTP-Method-Override':'GET',}
data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
