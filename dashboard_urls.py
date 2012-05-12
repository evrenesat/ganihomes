from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

#from website import dashboard as db

urlpatterns = patterns('website.dashboard',
        url(r'^$', "dashboard", name='dashboard'),
        url(r'^list_places/$', "list_places", name='list_places'),
        url(r'^show_faq/$', "show_faq", name='dashboard_faq'),
        url(r'^pfoto/$', "pfoto", name='pfoto'),
        url(r'^edit_payment/$', "edit_payment", name='edit_payment'),
        url(r'^show_messages/$', "show_messages", name='show_messages'),
        url(r'^show_requests/$', "show_requests", name='show_requests'),
        url(r'^show_reviews/$', "show_reviews", name='show_reviews'),
        url(r'^trips/$', "trips", name='trips'),
        url(r'^overview_messages/$', "show_messages", {'template':'dashboard/overview_messages.html'}, name='overview_messages'),
        url(r'^delete_place/$', "delete_place", name='delete_place'),
        url(r'^publish_place/$', "publish_place", name='publish_place'),
        url(r'^edit_profile/$', "edit_profile", name='edit_profile'),
        url(r'^change_password/$', "change_password", name='change_password'),
        url(r'^invite_friend/$', "invite_friend", name='invite_friend'),
        url(r'^support_create/$', "support_create", name='support_create'),
        url(r'^support_list/$', "support_list", name='support_list'),
        url(r'^support_show/$', "support_show", name='support_show'),
        url(r'^edit_description/(?P<pid>\d+)$', "edit_description", name='edit_description'),
        url(r'^confirm_friendship/$', "confirm_friendship", name='confirm_friendship'),
        url(r'^friends/$', "friends", name='friends'),
#        url(r'^list_places/(?P<type>[^/]+)/$', "list_places, name='list_places_bytype'),
        url(r'^edit_prices/(?P<id>\d+)$', "edit_prices", name='edit_prices'),
        url(r'^show_booking/(?P<id>\d+)$', "show_booking", name='show_booking'),
        (r'^review_place/(?P<id>\d+)/?$', 'review_place', {}, 'review_place'),
        (r'^review_guest/(?P<id>\d+)/?$', 'review_guest', {}, 'review_guest'),
        url(r'^new_message/(?P<id>\d+)$', "new_message", name='new_message'),
        url(r'^add_friend/(?P<id>\d+)$', "add_friend", name='add_friend'),
        url(r'^calendar/(?P<id>\d+)$', "calendar", name='calendar'),
        url(r'^show_message/(?P<id>\d+)$', "show_message", name='show_message'),
        url(r'^save_calendar/(?P<id>\d+)$', "save_calendar", name='save_calendar'),
        url(r'^save_photo_order/(?P<id>\d+)$', "save_photo_order", name='save_photo_order'),

    )

# vim: et sw=4 sts=4
