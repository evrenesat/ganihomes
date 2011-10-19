# -*- coding: utf-8 -*-
__author__ = 'Evren Esat Ozkan'
from places.options import LOCALES
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.cache import kes
from django.template.defaultfilters import slugify


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
    kelime = models.CharField(_('Anahtar Kelime'), max_length=100, help_text='En çok 100 karakter uzunluğunda olabilir')
    durum = models.SmallIntegerField(_('Durum'), choices=((0, 'Yok'), (1, 'Eksik'), (2, 'Tam')), default=0)
    # = models.IntegerField(_(''))
    # = models.SmallIntegerField(_(''))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        verbose_name = u"Çeviri"
        verbose_name_plural = u"Çeviriler"
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
    kod = models.CharField(_('Dil'), max_length=5, choices=LOCALES)
#    dil = models.SmallIntegerField(verbose_name=_('Dil'), choices=LOCALES)
    ceviri = models.TextField(_('Çevirisi'), help_text='En çok 100 karakter uzunluğunda olabilir')
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)


    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        app_label = 'website'
        verbose_name = u"Karşılık"
        verbose_name_plural = u"Karşılıklar"

    def __unicode__(self):
        return '%s' % (self.kelime,)


    #    @classmethod
    #    def _tum_ceviriler(cls,dil_kodu):

    @classmethod
    def cevir(cls, kelime, dil_kodu):
        skelime = slugify(kelime)

        k = kes(cls.KES_PREFIX, skelime[:40], dil_kodu)
        c = k.g()
        if c:
            return  c
        else:
            c = cls.objects.filter(asil=skelime, kod=dil_kodu).values_list('ceviri')

        if c:
            k.s(c[0][0])
            return c[0][0]
        else:
            c = cls.objects.filter(asil=skelime).values_list('ceviri')

        if c:
            k.s(c[0][0])
            return c[0][0]
        else:
            Kelime.objects.get_or_create(kelime=skelime)
            return kelime


    def save(self, *args, **kwargs):
        self.asil = self.kelime.kelime
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

