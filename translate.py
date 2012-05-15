    #! /usr/bin/env python
# -*-  coding: utf-8 -*-
from json import loads
import sys
import os
from time import sleep
from django.db.models import Count
import argparse
from django.conf import settings

pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.abspath(pathname))
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from applicationinstance import ApplicationInstance
from django.utils.translation import activate, force_unicode

from places.models import Place, Description
#from utils.cache import kes
#from utils.xml2dict import fromstring
DEVELOPER_KEY = 'AIzaSyAd8evO6SwmuE3RoBdaROzLoNGesc386Vg'
GOOGLE_TRANSLATE_URL = 'https://www.googleapis.com/language/translate/v2'
import logging
log = logging.getLogger('genel')
import httplib2
httplib2.debuglevel = 4

from configuration import configuration



import urllib
import urllib2






class TranslationMachine:
    """
    google translation machine
    """
    def __init__(self):
        self.auto_langs = configuration('auto_trans_langs').split(',')
        self.auto_lang_count = len(self.auto_langs)


#        self.run()

    def translator(self, query, target, source=None):
        try:
            values = [('key' , DEVELOPER_KEY),
                    ('target' , target),
                    ('q',query[0]),
                    ('q',query[1]),
            ]
            if source:
                values.append(('source',source))
            headers={'X-HTTP-Method-Override':'GET',}
            data = urllib.urlencode(values)
#            print data
            req = urllib2.Request(GOOGLE_TRANSLATE_URL, data, headers)
            response = urllib2.urlopen(req)
            sonuc =  loads(response.read())['data']['translations']
#            print 'sonuc',sonuc
            return sonuc
        except:
            log.exception('%s karakterlik ceviri sirasinda hata: %s %s' % (len(query[0]) + len(query[1]), query[0], query[1] ) )

    def trnsltr(self, query, target, source=None):
        try:
            values = [('key' , DEVELOPER_KEY),
                    ('target' , target),
                    ('q',query),

            ]
            if source:
                values.append(('source',source))
            headers={'X-HTTP-Method-Override':'GET',}
            data = urllib.urlencode(values)
#            print data
            req = urllib2.Request(GOOGLE_TRANSLATE_URL, data, headers)
            response = urllib2.urlopen(req)
            sonuc =  loads(response.read())['data']['translations']
#            print 'sonuc',sonuc
            return sonuc
            sleep(1)
        except:
            log.exception('%s karakterlik ceviri sirasinda hata: %s ' % (len(query), query ) )


    def run(self):
        self.generate_multiling_location_tags()
        self.translate_untranslateds()
        self.semitranslateds()

    def generate_multiling_location_tags(self):
        self.translate_location(Place.objects.filter(i18_tags__isnull=True, published=True, active=True))

    def translate_untranslateds(self):
        self.translate(Place.objects.filter(translated=False, published=True, active=True))

    def semitranslateds(self):
        pids = Place.objects.filter(active=True, published=True).annotate(Count('descriptions')).values_list('id','descriptions__count')
        ids = map(lambda x:x[0], filter(lambda p:p[1] < self.auto_lang_count ,pids))
        self.translate(Place.objects.filter(id__in=ids, published=True, active=True))

    def translate(self, places):
        for p in places:
            log.info('mekan: %s' % p)
            if self.translate_place(p):
                p.translated = True
                p.save()
                log.info('mekan cevrildi: %s ' % p)
            else:
                log.info('ceviri basarisiz: %s ' % p)
            p.get_translation_list(reset=True)
            sleep(1)

    def translate_location(self, places):
        for p in places:
            tags = set()
            for code,name in settings.LANGUAGES:
                activate(code)
                tags.add(p.get_country_display())
                tags.add(p.city)
#                print tags, p.city
                if code != p.lang:
                    tags.add(self.trnsltr(p.city, code, p.lang)[0]['translatedText'])
            t  = ' '.join(tags)
            if len(t)>255:
                log.info('COK UZUN: %s'% t)
                t = t[:255]
            p.i18_tags = t
            p.save()
#    def reTranslate(self):
#        '''yayindaki evlerin auto cevirilerini yeniden yapar.'''
#        for p in Place.objects.filter(translated=False, published=True, active=True):
#            for d in p.descriptions.filter(auto=True):
#                translation = self.translator([p.title,p.description.replace('\n','<br>')],d.lang)
#                d.text = translation[1]['translatedText'].replace('<br>','\n')
#                d.title = translation[0]['translatedText']
#                d.save()

    def translate_place(self,p):
        log.info('CEVRiLECEK: %s ' % p)
        success = 0
        for l in self.auto_langs:
            d, new = Description.objects.get_or_create(place=p, lang=l)
            if not(new or d.auto):
                  continue
            translation = self.translator([p.title,p.description.replace('\n','{0}')],l)
            if translation:
                d.text = translation[1]['translatedText'].format({})
                d.title = translation[0]['translatedText'][:99]
                d.auto = True
                d.save()
                success += 1
            elif new:
                d.delete()
        return success >= self.auto_lang_count / 2


#    def update_place_status(self, p):
#        translated_langs = p.get_translation_list(reset=True)
#        if translated_langs: #TODO: en az bir dil oldugu icin bu herzaman True oluyor.
#            status = p.translation_status
#            p.translation_status = 20
#            if all([ l in translated_langs for l in self.auto_langs ] ):
#                p.translation_status = 30
#            if status != p.translation_status :
#                p.save()
















if __name__ == '__main__':
    o = None
    inst = None
    try:
        inst = ApplicationInstance( '/tmp/gtranslate.pid' )

        o = TranslationMachine()
        o.run()
        if inst:
            inst.exitApplication()
    except SystemExit:
        if inst:
            inst.exitApplication()
        pass
    except:
        if inst:
            inst.exitApplication()
        log.exception('beklenmeyen hata')

