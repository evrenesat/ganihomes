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


from places.models import Place, Description
#from utils.cache import kes

DEVELOPER_KEY = 'AIzaSyAd8evO6SwmuE3RoBdaROzLoNGesc386Vg'
GOOGLE_TRANSLATE_URL = 'https://www.googleapis.com/language/translate/v2'
import logging
log = logging.getLogger('genel')
#import httplib2
#httplib2.debuglevel = 4

from configuration import configuration



import urllib
import urllib2






class TranslationMachine:
    """
    google translation machine
    """
    def __init__(self):
        self.auto_langs = configuration('auto_trans_langs').split(',')


        self.run()

    def translate(self, query, target, source=None):
        try:
            values = {'key' : DEVELOPER_KEY,
                      'target' : target,
                       'q':query}
            if source:
                values['source']=source
            headers={'X-HTTP-Method-Override':'GET',}
            data = urllib.urlencode(values)
            req = urllib2.Request(GOOGLE_TRANSLATE_URL, data, headers)
            response = urllib2.urlopen(req)
            print response.read()
            return
            return response.read()
        except:
            log.exception('unexpected error')


    def run(self):
#        print Place.objects.filter(translation_status__lt=30)
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
















if __name__ == '__main__':
    o = None
    inst = None
    try:
        inst = ApplicationInstance( '/tmp/gtranslate.pid' )

        o = TranslationMachine()
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

