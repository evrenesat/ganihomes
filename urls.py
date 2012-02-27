# -*- coding: utf-8 -*-

from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps import Sitemap
from places.models import Place

admin.autodiscover()
from django.conf.urls.defaults import *
handler500 = 'website.views.server_error'
from django.views.generic.simple import direct_to_template

class PlaceSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Place.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.last_modified

sitemaps = {
    'places': PlaceSitemap(),
}



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cagani.views.home', name='home'),
    # url(r'^cagani/', include('cagani.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^crossdomain.xml$', direct_to_template, {'template': 'crossdomain.xml'}),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
#    (r'^tinymce/', include('tinymce.urls')),
)

urlpatterns += patterns('website.views',
    (r'^dilsec/(?P<kod>[-\w]+)?/$', 'dilsec', {}, 'dilsec'),
    (r'^set_message/(?P<msg>[-\w]+)?$', 'set_message', {}, 'set_message'),

    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)?/$', 'icerik',{} , 'icerik'),
#    (r'iletisim/$', 'iletisim',{} , 'iletisim'),
    (r'mesaj_goster/$', 'mesaj_goster',{} , 'mesaj_goster'),
#    (r'banner/anasayfa.xml$', 'bannerxml',{'tip':1} , 'bannerxml'),
#    (r'banner/altsayfa.xml$', 'bannerxml',{'tip':2} , 'bannerxml'),
    (r'^registeration_thanks/$', 'registeration_thanks', {}, 'registeration_thanks'),
    (r'^login/$', 'login', {}, 'login'),
    (r'^505/$', 'server_error', {}, 'server_error'),
    (r'^404/$', 'server_error', {'template_name':'404.html'}, 'not_found'),

    (r'^password_reset/$', auth_views.password_reset, {}, 'password_reset'),
    (r'^logout/$', 'logout', {}, 'logout'),
    (r'^localeurl/', include('localeurl.urls')),
    (r'^login_or_register/$', 'register', {'template':'loginorregister.html'}, 'lregister'),
    (r'^register/$', 'register', {}, 'register'),
    (r'^faq/$', 'show_faqs', {}, 'faq'),

    (r'^ZXE/SDS/FSSS/SKTR/', include('paypal.standard.ipn.urls')),
    (r'^howitworks$', direct_to_template, {'template': 'howitworks.html'},'howitworks'),
    (r'^tips$', direct_to_template, {'template': 'tips.html'},'tips'),
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^dashboard/', include('dashboard_urls')),
    (r'^upload_photo/(?P<place_id>\d+)$', 'multiuploader', {}, 'upload_photo_toplace'),
    (r'^slides/(?P<id>\d+)/$', 'slides', {}, 'slides'),
    (r'^place_translation/(?P<id>\d+)/(?P<lang>[-\w]+)/$', 'place_translation', {}, 'place_translation'),
    (r'^upload_photo/$', 'multiuploader', {}, 'upload_photo'),
    (r'^delete_photo/(?P<pk>\d+)$', 'multiuploader_delete', {}, 'delete_photo'),
    (r'^status_check/$', 'statusCheck', {}, 'status_check'),
    (r'^jsearch/$', 'search_ajax', {}, 'jsearch'),
    (r'^jsearch/(?P<current_page>\d+)$', 'search_ajax', {}, 'jsearch-page'),
    (r'^search/$', 'search', {}, 'search'),
    (r'^bookmark/$', 'bookmark', {}, 'bookmark'),
    (r'^add_place_ajax/(?P<id>\d+)$', 'addPlace', {'ajax':True}, 'edit_place_ajax'),
    (r'^sac/$', 'search_autocomplete', {}, 'search_autocomplete'),
    (r'^add_place_ajax/$', 'addPlace', {'ajax':True}, 'add_place_ajax'),
    (r'^add_place/$', 'addPlace', {}, 'add_place'),
    (r'^send_message_to_host/$', 'send_message_to_host', {}, 'send_message_to_host'),
    (r'^places/(?P<id>\d+)/?$', 'showPlace', {}, 'show_place'),
    (r'^profiles/(?P<id>\d+)/?$', 'show_profile', {}, 'show_profile'),
    (r'^find_place/$', 'searchPlace', {}, 'search_place'),
    (r'^/?$', 'anasayfa', {}, 'anasayfa'),
    (r'^news/(?P<slug>[-\w]+)/(?P<id>\d+)/$', 'haber_goster',{} , 'haber_goster'),
)







urlpatterns += patterns('website.booking',
    (r'^book_place/$', 'book_place', {}, 'book_place'),
    (r'^secure_booking/$', 'secure_booking', {}, 'secure_booking'),
    (r'^paypal_checkout/$', 'paypal_checkout', {}, 'paypal_checkout'),
    (r'^paypal_return/$', 'paypal_complete', {}, 'paypal_complete'),
    (r'^bank_transfer_complete/$', 'bank_transfer_complete', {}, 'bank_transfer_complete'),
    (r'^paypal_cancel/$', 'paypal_cancel', {}, 'paypal_cancel'),

)


urlpatterns += patterns('support.views',
    url(r'^contact_us/$', 'contactUs',name='contact_us'),
    url(r'^contact_box/$', 'contact_box',name='contact_box'),
    (r'^close/(?P<id>\d+)$', 'AdminClose',{},'support_admin_close'),
    (r'^ticket/(?P<id>\d+)/$','AdminShow',{},'support_admin_show_ticket'),
    #url(r'^iletisim/(?P<subjectid>\d+)$', 'contactUs',name='contact_us'),
)



urlpatterns+=patterns('',
url(r'^tesekkurler', 'django.views.generic.simple.direct_to_template',{'template': 'contactus/thanks.html', 'extra_context':{'title':u'Teşekkürler'}}, name='contact_us_thanks'),
    )







if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

