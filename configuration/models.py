# -*- coding: utf-8 -*-
from configuration.modelbase import ConfigBase, models
from django.conf import settings

class Config(ConfigBase):
    email_activation = models.BooleanField(u'Eposta Onayı', help_text=u"Üyelik için eposta onayı gereksin mi?",
        default=False)
    host_fee = models.IntegerField(u'Ev Sahibi Komisyonu (%)', default=10,
        help_text=u"Mekan sahibinin girdiği tutardan kesilecek varsayılan komisyon oranı", null=True, blank=True)
    guest_fee = models.IntegerField(u'Misafir komisyonu (%)', default=2,
        help_text=u"Misafirlerden kesilecek komisyon oranı", null=True, blank=True)
    nasil_slide_zaman = models.CharField(u'Nasıl çalışır slide zamanları', default='1,4,10,20,30,-40,45', max_length=200
        , null=True, blank=True,
        help_text=u'''Slaytların gösterim zamanlarını saniye cinsinden  virgülle ayrılmış olarak giriniz. <br>
    Son slaytın gösterime girme saniyesinin başına - (eksi işareti) koymalısınız. <br>
    En sonada slaytın kaç saniye gösterildikten sonra başa dönüleceğini belirten bir sayı girilir.<br>
    Başa dönülmesini istemiyorsanız 0 girebilirsiniz.<br>
    örn: "<b>1, 30, -50, 60</b>" şeklindeki girdi, ilk slaydın <b>1.</b> saniyede,
    ikincisinin <b>30.</b> saniyede, son slaydın ise <b>50.</b> saniyede gösterilmesini sağlar. <b>60.</b> saniyede ise başa dönülür.
    <br> 60 yerine <b>0</b> yazılsaydı sunum orada kesilir, başa dönülmezdi.<br>
    Tek bir slayt göstermek istiyorsanız "-1,0" girmeniz yeterlidir.
    ''')
    iban_countries = models.TextField(u'IBAN\'ın yeterli olduğu ülkeler.', help_text="Orn: TR,DE,UK", null=True,
        blank=True, default='TR')
    listed_langs = models.TextField(u'Listelen Diller', default='en,English\ntr,Türkçe\nes,Español\nde,Deutsch\nit,Italiano',
        help_text=u'Sitede listelenecek dillerin 2 harfli ISO kodlarını ve dilin adını virgülle ayırıp, boşluk kullanmadan her satıra bir dil gelecek şekilde giriniz. <br>örn:<br>tr,Türkçe<br>en,English<br>es,Español.<br><b>NOT: Sadece şu diller içinden seçebilirsiniz: %s</b>' %
                  ', '.join([l[0] for l in settings.LANGUAGES])
    )
    trans_langs = models.CharField(u'Çevirisi yapılabilecek diller', max_length=200, default='tr,en,es,fr,de',
        help_text=u'Dil kodlarını 2 harfli ISO standardına göre virgüle ayırarak giriniz. Örn: tr,en,es,fr,de .',
        null=True, blank=True)
    auto_trans_langs = models.CharField(u'Otomatik çevirisi yapılacak diller', max_length=200, default='tr,en,es,fr,de',
        help_text=u'Dil kodlarını 2 harfli ISO standardına göre virgüle ayırarak giriniz. Örn: tr,en,es,fr,de',
        null=True, blank=True)
#    pos_deniz_bank = models.CharField(u'Otomatik çevirisi yapılacak diller', max_length=200, default='tr,en,es,fr,de',
#        help_text=u'Dil kodlarını 2 harfli ISO standardına göre virgüle ayırarak giriniz. Örn: tr,en,es,fr,de',
#        null=True, blank=True)




