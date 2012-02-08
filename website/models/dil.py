# -*- coding: utf-8 -*-
from django.conf import settings

__author__ = 'Evren Esat Ozkan'
from places.options import LOCALES
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.cache import kes
from django.template.defaultfilters import slugify
import logging
log = logging.getLogger('genel')


#class Dil(models.Model):
#    """
#    belgelendirme eksik !!!!!!!!
#    """
#    CACHE_KEY = 'etkin_diller'
#    etkin = models.BooleanField(u"Etkin mi?", default=True)
#    pul = models.DateTimeField(u"Kayıt Zamanı", auto_now_add=True)
#    adi = models.CharField(u"Dil Adı", max_length=30, help_text='"')
#    kodu = models.CharField(u"Dil Kodu", max_length=5)
#
#
#    def __unicode__(self):
#        return self.adi
#
#
#    class Meta:
#        verbose_name = u"Dil"
#        verbose_name_plural = u"Diller"
#        app_label = 'website'
#        #ordering = []
#        #get_latest_by=''
#        #order_with_respect_to = ''
#        #unique_together = (("", ""),)
#        #permissions = (("can_do_something", "Can do something"),)
#
#    @classmethod
#    def etkin_diller(cls):
#        return kes(cls.CACHE_KEY).g(cls.onbellekle())
#
#    @classmethod
#    def onbellekle(cls):
#        diller = cls.objects.filter(etkin=True).values_list('kodu', 'adi')
#        kes(cls.CACHE_KEY).s(diller)
#        return diller
#
#
#    def save(self, *args, **kwargs):
#        super(Dil, self).save(*args, **kwargs)
#        Dil.onbellekle()


class Kelime(models.Model):
    """Çevrilecek kelime"""

    # = models.ForeignKey(, verbose_name=_(''))
    kelime = models.CharField(_('Anahtar Kelime'), max_length=100, help_text='<ul><li>En çok 100 karakter uzunluğunda olabilir<li>Ne yaptığınızdan emin değilseniz mevcut anahtar kelimeleri değiştirmeyiniz.</ul>')
    durum = models.SmallIntegerField(_('Durum'), choices=((0, 'Yok'), (1, 'Eksik'), (2, 'Tam')), default=0)
    # = models.IntegerField(_(''))
    # = models.SmallIntegerField(_(''))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)


    def save(self, *args, **kwargs):
        super(Kelime, self).save(*args, **kwargs)
        for k,n in settings.LANGUAGES:
            cset = self.ceviriler_set.filter(kod=k)
            if not cset:
                self.ceviriler_set.create(kod=k)

    class Meta:
        verbose_name = u"İçerik Bloku"
        verbose_name_plural = u"İçerik Blokları"
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        app_label = 'website'
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.kelime,)


class Ceviriler(models.Model):
    """basit ceviri sistemi"""
    KES_PREFIX = 'CEVIR'

    kelime = models.ForeignKey(Kelime, verbose_name=_('Türkçesi'))
    asil = models.CharField(max_length=100, editable=False)
    kod = models.CharField(_('Dil'), max_length=5, choices=settings.LANGUAGES)
#    dil = models.SmallIntegerField(verbose_name=_('Dil'), choices=LOCALES)
    ceviri = models.TextField(_('Çevirisi'), default='', blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)


    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        app_label = 'website'
        verbose_name = u"Karşılık"
        verbose_name_plural = u"Karşılıklar"

    def __unicode__(self):
        return '%s' % (self.asil,)


    #    @classmethod
    #    def _tum_ceviriler(cls,dil_kodu):

    @classmethod
    def cevir(cls, kelime, dil_kodu):
        try:
            skelime = slugify(kelime)
            k = kes(cls.KES_PREFIX, skelime[:40], dil_kodu)
            c = k.g()
            if c: return  c
            c = cls.objects.filter(asil=skelime, kod=dil_kodu).exclude(ceviri='').values_list('ceviri',flat=True)
            if c: return k.s(c[0])
    #        c = cls.objects.filter(asil=skelime).exclude(ceviri='').values_list('ceviri',flat=True)
    #        if c: return k.s(c[0])
            Kelime.objects.get_or_create(kelime=skelime)
            return k.s(kelime)
        except:
            log.exception('cevir taginda patlama')
            return kelime

    def save(self, *args, **kwargs):
        self.asil = slugify(self.kelime.kelime)
#        self.kod = self.dil.kodu
        super(Ceviriler, self).save(*args, **kwargs)
        ceviri_sayisi = self.kelime.ceviriler_set.exclude(ceviri='').count()
        durum = 0
        if ceviri_sayisi:
            durum = 2 if ceviri_sayisi == len(LOCALES) else 1
        if self.kelime.durum != durum:
            self.kelime.durum = durum
            self.kelime.save()
        kes(self.KES_PREFIX, self.asil, self.kod).s(self.ceviri)

