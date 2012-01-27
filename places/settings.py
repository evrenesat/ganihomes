# -*- coding: utf-8 -*-
import appsettings

from django import forms
register = appsettings.register('gh')

# settings are organized into groups.
# this will define settings
#   mymodule.story.greeting,
#   mymodule.story.pigs,
#   etc.

#    wolves = 1
    # or you can specify the type
#    houses = forms.IntegerField(initial = 3, doc = "number of houses in which to hide")
#    myhouse = forms.ChoiceField(choices = (('straw', 'Straw'),
#                                         ('sticks', 'Sticks'),
#                                         ('bricks', 'Bricks')),
#                                initial = 'straw')



class Usr:
    # int, string, and float types are auto-discovered.

    email_activation = forms.BooleanField(label=u'Eposta Onayı', initial = 10,  help_text = u"Üyelik için eposta onayı gereksin mi?")

Usr = register(Usr)

class Globals:
    # int, string, and float types are auto-discovered.
    host_fee = forms.IntegerField(label=u'Ev Sahibi Komisyonu (%)', initial = 10,  help_text = u"Mekan sahibinin girdiği tutardan kesilecek varsayılan komisyon oranı")
    guest_fee = forms.IntegerField(label=u'Misafir komisyonu (%)', initial = 10,  help_text = u"Misafirlerden kesilecek komisyon oranı")
    nasil_slide_zaman = forms.CharField(label=u'Nasıl çalışır slide zamanları', initial='0',  help_text = u'''Slaytların gösterim zamanlarını saniye cinsinden  virgülle ayrılmış olarak giriniz. <br>
    Son slaytın gösterime girme saniyesinin başına - (eksi işareti) koymalısınız. <br>
    En sonada slaytın kaç saniye gösterildikten sonra başa dönüleceğini belirten bir sayı girilir.<br>
    Başa dönülmesini istemiyorsanız 0 girebilirsiniz.<br>
    örn: "<b>1, 30, -50, 60</b>" şeklindeki girdi, ilk slaydın <b>1.</b> saniyede,
    ikincisinin <b>30.</b> saniyede, son slaydın ise <b>50.</b> saniyede gösterilmesini sağlar. <b>60.</b> saniyede ise başa dönülür.
     <br> 60 yerine <b>0</b> yazılsaydı sunum orada kesilir, başa dönülmezdi.<br>
     Tek bir slayt göstermek istiyorsanız "-1,0" girmeniz yeterlidir.
    ''')

Globals = register(main=True)(Globals)

