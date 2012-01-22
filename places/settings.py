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
    nasil_slide_zaman = forms.CharField(label=u'Nasıl çalışır slide zamanları', initial='0',  help_text = u"Saniye cinsinden  virgülle ayrılmış olarak giriniz. 1,14,50,90 gibi.")

Globals = register(main=True)(Globals)

