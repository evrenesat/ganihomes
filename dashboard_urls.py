from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from website import dashboard as db

urlpatterns = patterns('',
        url(r'^list_places/$', db.list_places, name='list_places'),
        url(r'^show_faq/$', db.show_faq, name='dashboard_faq'),
        url(r'^pfoto/$', db.pfoto, name='pfoto'),
        url(r'^edit_payment/$', db.edit_payment, name='edit_payment'),
        url(r'^show_messages/$', db.show_messages, name='show_messages'),
        url(r'^edit_profile/$', db.edit_profile, name='edit_profile'),
#        url(r'^list_places/(?P<type>[^/]+)/$', db.list_places, name='list_places_bytype'),
        url(r'^edit_prices/(?P<id>\d+)$', db.edit_prices, name='edit_prices'),
    )

# vim: et sw=4 sts=4
