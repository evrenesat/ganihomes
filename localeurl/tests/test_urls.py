"""
URLconf for testing.
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('localeurl.tests.test_urls',
     url(r'^dummy/$', 'dummy', name='dummy0'),
     url(r'^dummy/(?P<test>.+)$', 'dummy', name='dummy1'),
)

def dummy(request, test='test'):
    pass
