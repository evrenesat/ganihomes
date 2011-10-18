from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cagani.views.home', name='home'),
    # url(r'^cagani/', include('cagani.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
)

urlpatterns += i18n_patterns('website.views',
    (r'^dilsec/(?P<kod>[-\w]+)?/$', 'dilsec', {}, 'dilsec'),

    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)?/$', 'icerik',{} , 'icerik'),
    (r'iletisim/(?P<urun_id>\d+)/$', 'iletisim',{} , 'iletisim'),
    (r'iletisim/$', 'iletisim',{} , 'iletisim'),
    (r'mesaj_goster/$', 'mesaj_goster',{} , 'mesaj_goster'),
    (r'banner/anasayfa.xml$', 'bannerxml',{'tip':1} , 'bannerxml'),
    (r'banner/altsayfa.xml$', 'bannerxml',{'tip':2} , 'bannerxml'),
    (r'^/?$', 'anasayfa', {}, 'anasayfa'),
    (r'^news/(?P<slug>[-\w]+)/(?P<id>\d+)/$', 'haber_goster',{} , 'haber_goster'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

