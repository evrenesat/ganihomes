# -*- coding: utf-8 -*-
from django.db.models.query_utils import Q
from places.options import LOCALES

__author__ = 'Evren Esat Ozkan'
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
import time


def upload_to(instance, filename):
    tip_int, uzanti = instance.dosya_tipi_bul(filename)
    dosya_ad = slugify(instance.ad if instance.ad else filename.replace('.%s' % uzanti, ''))
    return '%s/%s_%s.%s' %  (slugify(dict(Medya.TIP_SECENEKLERI)[tip_int]), int(round(time.time())), dosya_ad, uzanti )

class DosyaManager(models.Manager):
    def __init__(self, tip):
        self.tip = tip
        super(DosyaManager, self).__init__()
    def get_query_set(self):
        return super(DosyaManager, self).get_query_set().filter(tip=self.tip ,etkin=True)


class Medya(models.Model):
    """
    belgelendirme eksik !!!!!!!!
    """
    TIP = ((1,'Görsel','jpg,jpeg,png,bmp,gif'),(2,'Video','flv,ogv,mp4'),(3,'Belge','pdf'),(4,u'Diğer',''),)
    TIP_SECENEKLERI = map(lambda x:(x[0],x[1]), TIP)
    tip = models.SmallIntegerField(_('Dosya Tipi'), choices=TIP_SECENEKLERI, db_index=True)
    ad = models.CharField(_(u'Dosya Adı'),max_length=185)
#    dil=models.ForeignKey(Dil , null=True, blank=True)
    pul = models.DateTimeField(u"Kayıt Zamanı", auto_now_add=True)
    sablon = models.CharField(max_length=200, null=True, blank=True,choices=[('',u'Seçiniz'),],help_text=u'Yüklediğiniz dosyanın özel bir biçimde gösterilmesi için farklı bir gösterim şablonu seçebilirsiniz.. <br><b>!!! Emin değilseniz bu ayarı değiştirmeyiniz !!!</b>', editable=False)
    etkin = models.BooleanField(u"Etkin", default=True, help_text=u"İçerik yayınlansın mı?", db_index=True)
    dosya = models.FileField(_('Dosya'), upload_to=upload_to)
    dil_kodu = models.CharField(max_length=5, choices=LOCALES)

    objects = models.Manager() # The default manager.
    gorseller = DosyaManager(1)
    videolar = DosyaManager(2)
    belgeler = DosyaManager(3)

    @classmethod
    def dbelgeler(cls,dilkodu):
        return cls.belgeler.filter(Q(dil_kodu=dilkodu)|Q(dil_kodu__isnull=True))
    @classmethod
    def dgorseller(cls,dilkodu):
        return cls.gorseller.filter(Q(dil_kodu=dilkodu)|Q(dil_kodu__isnull=True))
    @classmethod
    def dvideolar(cls,dilkodu):
        return cls.videolar.filter(Q(dil_kodu=dilkodu)|Q(dil_kodu__isnull=True))

    #= models.CharField(u"",max_length=)
    #= models.SmallIntegerField(u"")
    #= models.IntegerField(u"")
    #= models.DecimalField(u"", max_digits=4, default=Decimal('0.0'),  decimal_places=2, )
    #= models.TextField(u"",help_text="",null=True,blank=True)
    #= models.DateField(u"", null=True, blank=True)
    #= models.DateTimeField(u"",  null=True,  blank=True )


    def __unicode__(self):
        return  '%s > %s' % ( self.get_tip_display(), self.ad )




    class Meta:
        verbose_name = u"Medya Dosyasi"
        verbose_name_plural = u"Medya Dosyaları"
        app_label = 'website'

    @classmethod
    def dosya_tipi_bul(cls, dosyaadi):
        tip_int = 4  #diger
        uzanti = dosyaadi.split('.')[-1]
        for t in cls.TIP:
            if uzanti in t[2]:
                tip_int = t[0]
                break
        return tip_int, uzanti

    def tip_duzelt(self):
        self.tip,uza = self.dosya_tipi_bul(self.dosya.name)
#        self.save()

    def save(self, *args, **kwargs):
#        if self.dil:
#            self.dil_kodu = self.dil.kodu
        if not self.id:
            self.tip_duzelt()
        super(Medya, self).save(*args, **kwargs)
