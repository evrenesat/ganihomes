from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from website import dashboard as db

urlpatterns = patterns('',
        url(r'^list_places/$', db.list_places, name='list_places'),
        url(r'^pfoto/$', db.pfoto, name='pfoto'),
        url(r'^edit_profile/$', db.edit_profile, name='edit_profile'),
        url(r'^list_places/(?P<type>[^/]+)/$', db.list_places, name='list_places_bytype'),
    )

# vim: et sw=4 sts=4
