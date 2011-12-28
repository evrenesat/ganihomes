# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf.urls.defaults import *
handler500 = 'website.views.server_error'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cagani.views.home', name='home'),
    # url(r'^cagani/', include('cagani.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^crossdomain.xml$', 'django.views.generic.simple.direct_to_template', {'template': 'crossdomain.xml'}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
)

urlpatterns += patterns('website.views',
    (r'^dilsec/(?P<kod>[-\w]+)?/$', 'dilsec', {}, 'dilsec'),

    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)?/$', 'icerik',{} , 'icerik'),
#    (r'iletisim/$', 'iletisim',{} , 'iletisim'),
    (r'mesaj_goster/$', 'mesaj_goster',{} , 'mesaj_goster'),
#    (r'banner/anasayfa.xml$', 'bannerxml',{'tip':1} , 'bannerxml'),
#    (r'banner/altsayfa.xml$', 'bannerxml',{'tip':2} , 'bannerxml'),
    (r'^registeration_thanks/$', 'registeration_thanks', {}, 'registeration_thanks'),
    (r'^login/$', 'login', {}, 'login'),
    (r'^505/$', 'server_error', {}, 'server_error'),
    (r'^404/$', 'server_error', {'template_name':'404.html'}, 'not_found'),
    (r'^ZXE/SDS/FSSS/SKTR/', include('paypal.standard.ipn.urls')),
    (r'^logout/$', 'logout', {}, 'logout'),
    (r'^localeurl/', include('localeurl.urls')),
    (r'^dashboard/$', 'dashboard', {}, 'dashboard'),
    (r'^login_or_register/$', 'register', {'template':'loginorregister.html'}, 'lregister'),
    (r'^register/$', 'register', {}, 'register'),
    (r'^book_place/$', 'book_place', {}, 'book_place'),
    (r'^ppreturn/$', 'paypal_complete', {}, 'paypal_complete'),
    (r'^ppcancel/$', 'paypal_cancel', {}, 'paypal_cancel'),
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^upload_photo/(?P<place_id>\d+)$', 'multiuploader', {}, 'upload_photo_toplace'),
    (r'^upload_photo/$', 'multiuploader', {}, 'upload_photo'),
    (r'^delete_photo/(?P<pk>\d+)$', 'multiuploader_delete', {}, 'delete_photo'),
    (r'^status_check/$', 'statusCheck', {}, 'status_check'),
    (r'^jsearch/$', 'search_ajax', {}, 'jsearch'),
    (r'^search/$', 'search', {}, 'search'),
    (r'^add_place_ajax/(?P<id>\d+)$', 'addPlace', {'ajax':True}, 'edit_place_ajax'),
    (r'^sac/$', 'search_autocomplete', {}, 'search_autocomplete'),
    (r'^add_place_ajax/$', 'addPlace', {'ajax':True}, 'add_place_ajax'),
    (r'^add_place/$', 'addPlace', {}, 'add_place'),
    (r'^places/(?P<id>\d+)$', 'showPlace', {}, 'show_place'),
    (r'^find_place/$', 'searchPlace', {}, 'search_place'),
    (r'^/?$', 'anasayfa', {}, 'anasayfa'),
    (r'^news/(?P<slug>[-\w]+)/(?P<id>\d+)/$', 'haber_goster',{} , 'haber_goster'),
)







urlpatterns += patterns('support.views',
    url(r'^iletisim/$', 'contactUs',name='contact_us'),
    #url(r'^iletisim/(?P<subjectid>\d+)$', 'contactUs',name='contact_us'),
)



urlpatterns+=patterns('',
url(r'^tesekkurler', 'django.views.generic.simple.direct_to_template',{'template': 'contactus/thanks.html', 'extra_context':{'title':u'Teşekkürler'}}, name='contact_us_thanks'),
    )







if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

