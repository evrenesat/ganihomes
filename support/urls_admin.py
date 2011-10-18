from django.conf.urls.defaults import *


urlpatterns = patterns('support.views',
    (r'^close/$', 'AdminClose',{},'support_admin_close'),
    (r'^ticket/(?P<id>\d+)/$','AdminShow',{},'support_admin_show_ticket'),
)
