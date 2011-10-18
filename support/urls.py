from django.conf.urls.defaults import *


urlpatterns = patterns('support.views',
    (r'^liste/$', 'List',{},'support_list'),
    (r'^istegi/$', 'Post',{},'support_compose'),
    (r'^goster/(?P<id>\d+)/$', 'Show',{},'support_show_ticket'),
    (r'^kapat/(?P<id>\d+)/$', 'AdminClose',{},'support_admin_close'),
    (r'^soru/(?P<id>\d+)/$','AdminShow',{},'support_admin_show_ticket'),
)

urlpatterns+=patterns('',
(r'^tesekkurler/$', 'django.views.generic.simple.direct_to_template', {'template': 'support/thanks.html'}, 'support_thanks'),
      )
