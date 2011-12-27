# -*-  coding: utf-8 -*-
__author__ = 'Evren Esat Ozkan'

#import memcache
from django.core.cache import cache
#cache = memcache.Client(['127.0.0.1:11211'], debug=0)
from django.conf import settings

from django.utils.encoding import smart_unicode, smart_str

sitekey = settings.CACHE_MIDDLEWARE_KEY_PREFIX
#sure = settings.CACHE_MIDDLEWARE_SECONDS
sure = 30

class kes:
    def __init__(self, *args):
        list(args).insert(0,sitekey)
        self.key = smart_str('_'.join([str(n) for n in args]))

    def __unicode__(self):
        return '%s icin onbellek nesnesi' % self.key


    def g(self, default=None):
        '''
        cacheden donen degeri, o yoksa `default` degeri dondurur
        '''
        d = cache.get(self.key)
        return d if d is not None else default

    def s(self, val=1, lifetime=sure):
        '''
        val :: atanacak deger (istege bagli bossa 1 atanir).
        lifetime :: önbellek süresi, varsayilan 100saat
        '''
        cache.set(self.key, val, lifetime)
        return val

    def d(self, *args):
        '''
        cache degerini temizler
        '''
        return cache.delete(self.key)

    def incr(self, delta=1):
        '''
        degeri delta kadar arttirir
        '''
        return cache.incr(self.key, delta=delta)

    def decr(self, delta=1):
        '''
        degeri delta kadar azaltir
        '''
        return cache.decr(self.key, delta=delta)
