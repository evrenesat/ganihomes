# -*- coding: utf-8 -*-
"""
Tests for the localeurl application.
"""
import re

from django import template
from django.core import urlresolvers
from django.test import TestCase
from django.utils import translation

from localeurl import middleware, settings as localeurl_settings, utils
from localeurl.models import reverse
from localeurl.sitemaps import LocaleurlSitemap
from localeurl.templatetags import localeurl_tags
from localeurl.tests import test_utils



def settings_fixture(mgr):
    mgr.set(
        USE_I18N = True,
        LANGUAGES = (
            ('en', 'English'),
            ('nl-nl', 'Dutch'),
            ('nl-be', 'Flemish'),
            ('fr', 'French'),
            ('pt', 'Portuguese'),
            ('pt-br', 'Brazilian Portuguese'),
        ),
        LANGUAGE_CODE = 'en-gb',
        LOCALE_INDEPENDENT_PATHS = (
            re.compile('^/$'),
            '^/test/independent/',
        ),
        LOCALE_INDEPENDENT_MEDIA_URL = True,
        MEDIA_URL = '/media/',
        LOCALE_INDEPENDENT_STATIC_URL = True,
        STATIC_URL = '/static/',
        TEMPLATE_CONTEXT_PROCESSORS = (
            'django.core.context_processors.i18n',
        ),
    )



class LocaleurlTestCase(TestCase):
    urls = 'localeurl.tests.test_urls'


    def setUp(self):
        self.settings_manager = test_utils.TestSettingsManager()
        settings_fixture(self.settings_manager)
        translation.activate("en")
        reload(localeurl_settings)
        reload(urlresolvers)


    def tearDown(self):
        self.settings_manager.revert()
        reload(localeurl_settings)
        reload(urlresolvers)



class UtilsTestCase(LocaleurlTestCase):
    def test_is_locale_independent(self):
        self.assertFalse(utils.is_locale_independent('/fr/about'))
        self.assertFalse(utils.is_locale_independent('/about'))
        self.assertTrue(utils.is_locale_independent('/media/img/logo.png'))
        self.assertTrue(utils.is_locale_independent('/static/img/logo.png'))
        self.assertTrue(utils.is_locale_independent('/'))
        self.assertTrue(utils.is_locale_independent(
                '/test/independent/bla/bla'))


    def test_strip_path(self):
        self.assertEqual(('', '/'), utils.strip_path('/'))
        self.assertEqual(('', '/about/'), utils.strip_path('/about/'))
        self.assertEqual(('', '/about/localeurl/'),
                utils.strip_path('/about/localeurl/'))
        self.assertEqual(('fr', '/about/localeurl/'),
                utils.strip_path('/fr/about/localeurl/'))
        self.assertEqual(('nl-be', '/about/localeurl/'),
                utils.strip_path('/nl-be/about/localeurl/'))
        self.assertEqual(('', '/de/about/localeurl/'),
                utils.strip_path('/de/about/localeurl/'))


    def test_strip_path_takes_longer_code_first(self):
        # Refs issue #15.
        self.assertEqual(('pt-br', '/about/localeurl/'),
                utils.strip_path('/pt-br/about/localeurl/'))


    def test_supported_language(self):
        self.assertEqual('fr', utils.supported_language('fr'))
        self.assertEqual('nl-be', utils.supported_language('nl-be'))
        self.assertEqual('en', utils.supported_language('en-gb'))
        self.assertEqual(None, utils.supported_language('de'))


    def test_is_default_locale(self):
        self.assertTrue(utils.is_default_locale('en'))
        self.assertFalse(utils.is_default_locale('en-gb'))
        self.assertFalse(utils.is_default_locale('fr'))
        self.assertFalse(utils.is_default_locale('de'))


    def test_locale_path(self):
        self.assertEqual('/en/about/localeurl/',
                utils.locale_path('/about/localeurl/'))
        self.assertEqual('/en/about/localeurl/',
                utils.locale_path('/about/localeurl/', 'de'))
        self.assertEqual('/en/about/localeurl/',
                utils.locale_path('/about/localeurl/', 'en'))
        self.assertEqual('/en/about/localeurl/',
                utils.locale_path('/about/localeurl/', 'en-us'))
        self.assertEqual('/nl-nl/about/localeurl/',
                utils.locale_path('/about/localeurl/', 'nl-nl'))
        self.assertEqual('/test/independent/bla/bla',
                utils.locale_path('/test/independent/bla/bla', 'en'))


    def test_locale_url(self):
        previous_script_prefix = urlresolvers.get_script_prefix()
        urlresolvers.set_script_prefix("/blah/")
        self.assertEqual('/blah/en/about/localeurl/',
                utils.locale_url('/about/localeurl/'))
        self.assertEqual('/blah/en/about/localeurl/',
                utils.locale_url('/about/localeurl/', 'de'))
        self.assertEqual('/blah/en/about/localeurl/',
                utils.locale_url('/about/localeurl/', 'en'))
        self.assertEqual('/blah/en/about/localeurl/',
                utils.locale_url('/about/localeurl/', 'en-us'))
        self.assertEqual('/blah/nl-nl/about/localeurl/',
                utils.locale_url('/about/localeurl/', 'nl-nl'))
        self.assertEqual('/blah/test/independent/bla/bla',
                utils.locale_url('/test/independent/bla/bla', 'en'))
        urlresolvers.set_script_prefix(previous_script_prefix)



class MiddlewareTestCase(LocaleurlTestCase):
    def setUp(self):
        super(MiddlewareTestCase, self).setUp()
        self.request_factory = test_utils.RequestFactory()
        self.middleware = middleware.LocaleURLMiddleware()


    def test_with_locale(self):
        r1 = self.request_factory.get('/fr/test/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(None, r2)
        self.assertEqual('fr', r1.LANGUAGE_CODE)
        self.assertEqual('/test/', r1.path_info)


    def test_with_sublocale(self):
        r1 = self.request_factory.get('/nl-nl/test/bla/bla/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(None, r2)
        self.assertEqual('nl-nl', r1.LANGUAGE_CODE)
        self.assertEqual('/test/bla/bla/', r1.path_info)


    def test_locale_independent_url(self):
        r1 = self.request_factory.get('/test/independent/bla/bla/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(None, r2)
        self.assertEqual('en-gb', r1.LANGUAGE_CODE)
        self.assertEqual('/test/independent/bla/bla/', r1.path_info)


    def test_locale_specified_on_independent_url_with_query_string(self):
        r1 = self.request_factory.get('/nl-be/test/independent/?foo=bar')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)
        self.assertEqual('/test/independent/?foo=bar', r2['Location'])


    def test_redirect_with_script_prefix(self):
        previous_script_prefix = urlresolvers.get_script_prefix()
        urlresolvers.set_script_prefix('/prefix/')

        r1 = self.request_factory.get('/nl-be/test/independent/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)
        self.assertEqual('/prefix/test/independent/', r2['Location'])

        # no infinite redirects
        r3 = self.request_factory.get('/test/independent/')
        r4 = self.middleware.process_request(r3)
        self.assertEqual(None, r4)

        urlresolvers.set_script_prefix(previous_script_prefix)


    def test_redirect_statuscode_302(self):
        self.settings_manager.set(LOCALE_REDIRECT_PERMANENT=False)
        reload(localeurl_settings)

        r1 = self.request_factory.get('/nl-be/test/independent/?foo=bar')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(302, r2.status_code)


    def test_redirect_statuscode_default(self):
        r1 = self.request_factory.get('/nl-be/test/independent/?foo=bar')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)


    def test_check_accept_lang(self):
        self.settings_manager.set(LOCALEURL_USE_ACCEPT_LANGUAGE=True)
        reload(localeurl_settings)

        r1 = self.request_factory.get('/test/', HTTP_ACCEPT_LANGUAGE='fr, de;q=0.8')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)
        self.assertEqual('/fr/test/', r2['Location'])



class DefaultPrefixMiddlewareTestCase(MiddlewareTestCase):
    def setUp(self):
        super(DefaultPrefixMiddlewareTestCase, self).setUp()


    def test_no_locale(self):
        r1 = self.request_factory.get('/test/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)
        self.assertEqual('/en/test/', r2['Location'])


    def test_non_ascii(self):
        r1 = self.request_factory.get('/plaît/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)
        self.assertEqual('/en/pla%C3%AEt/', r2['Location'])


    def test_with_query_string(self):
        r1 = self.request_factory.get('/test/?somevar=someval')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)
        self.assertEqual('/en/test/?somevar=someval', r2['Location'])



class NoDefaultPrefixMiddlewareTestCase(MiddlewareTestCase):
    def setUp(self):
        super(NoDefaultPrefixMiddlewareTestCase, self).setUp()
        self.settings_manager.set(PREFIX_DEFAULT_LOCALE=False)
        reload(localeurl_settings)


    def test_default_locale(self):
        r1 = self.request_factory.get('/test/foo/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(None, r2)
        self.assertEqual('en-gb', r1.LANGUAGE_CODE)
        self.assertEqual('/test/foo/', r1.path_info)


    def test_default_locale_specified(self):
        r1 = self.request_factory.get('/en/test/foo/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(301, r2.status_code)
        self.assertEqual('/test/foo/', r2['Location'])


    def test_alternate_locale(self):
        r1 = self.request_factory.get('/fr/test/foo/')
        r2 = self.middleware.process_request(r1)
        self.assertEqual(None, r2)
        self.assertEqual('fr', r1.LANGUAGE_CODE)
        self.assertEqual('/test/foo/', r1.path_info)



class TagsTestCase(LocaleurlTestCase):
    def render_template(self, text):
        t = test_utils.TestTemplate(text, libraries=[localeurl_tags.register])
        c = template.Context()
        return t.render(c)


    def test_locale_url_tag(self):
        self.assertRaises(ValueError, self.render_template,
                '{% locale_url "nl" dummy0 %}')

        self.assertEqual('/en/dummy/', self.render_template(
                '{% locale_url "en-us" dummy0 %}'))

        self.assertEqual('/fr/dummy/4', self.render_template(
            '{% locale_url "fr" dummy1 test=4 %}'))

        self.assertEqual('/en/dummy/4', self.render_template(
            '{% locale_url "en" dummy1 test=4 as testvar %}{{ testvar }}'))


    def test_chlocale_filter(self):
        self.assertEqual('/fr/dummy/', self.render_template(
                '{{ "/dummy/"|chlocale:"fr" }}'))

        self.assertEqual('/en/dummy/', self.render_template(
                '{{"/fr/dummy/"|chlocale:"en-gb"}}'))


    def test_rmlocale_filter(self):
        self.assertEqual('/dummy/', self.render_template(
                '{{ "/dummy/"|rmlocale }}'))

        self.assertEqual('/dummy/', self.render_template(
                '{{ "/nl-be/dummy/"|rmlocale }}'))

        self.assertEqual('/dummy/', self.render_template(
                '{{ "/en/dummy/"|rmlocale }}'))


    def test_locale_url_tag_no_default_prefix(self):
        self.settings_manager.set(PREFIX_DEFAULT_LOCALE=False)
        reload(localeurl_settings)

        self.assertEqual('/dummy/', self.render_template(
                '{% locale_url "en-us" dummy0 %}'))

        self.assertEqual('/fr/dummy/', self.render_template(
            '{% locale_url "fr" dummy0 %}'))


    def test_chlocale_filter_no_default_prefix(self):
        self.settings_manager.set(PREFIX_DEFAULT_LOCALE=False)
        reload(localeurl_settings)

        self.assertEqual('/dummy/', self.render_template(
                '{{ "/nl-nl/dummy/"|chlocale:"en-gb" }}'))

        self.assertEqual('/fr/dummy/', self.render_template(
                '{{"/nl-nl/dummy/"|chlocale:"fr"}}'))

try:
    from localeurl.templatetags import localeurl_future
except ImportError:
    localeurl_future = None


# @@@ use proper test skipping once Django 1.2 is minimum version
if localeurl_future is not None:
    class FutureTagsTestCase(LocaleurlTestCase):
        def render_template(self, text):
            t = test_utils.TestTemplate(text, libraries=[localeurl_future.register])
            c = template.Context()
            return t.render(c)


        def test_locale_url_tag(self):
            self.assertRaises(ValueError, self.render_template,
                    '{% locale_url "nl" "dummy0" %}')

            self.assertEqual('/en/dummy/', self.render_template(
                    '{% locale_url "en-us" "dummy0" %}'))

            self.assertEqual('/fr/dummy/4', self.render_template(
                '{% locale_url "fr" "dummy1" test=4 %}'))

            self.assertEqual('/en/dummy/4', self.render_template(
                '{% locale_url "en" "dummy1" test=4 as testvar %}{{ testvar }}'))


        def test_locale_url_tag_no_default_prefix(self):
            self.settings_manager.set(PREFIX_DEFAULT_LOCALE=False)
            reload(localeurl_settings)

            self.assertEqual('/dummy/', self.render_template(
                    '{% locale_url "en-us" "dummy0" %}'))

            self.assertEqual('/fr/dummy/', self.render_template(
                '{% locale_url "fr" "dummy0" %}'))



class DummyModel(object):
    def __init__(self, num):
        self.num = num


    def get_absolute_url(self):
        return '/dummy/%s/' % self.num



class DummySitemap(LocaleurlSitemap):
    def items(self):
        return [DummyModel(i) for i in range(3)]



class SitemapTestCase(LocaleurlTestCase):
    def setUp(self):
        super(SitemapTestCase, self).setUp()
        class DummySite(object):
            domain = 'www.example.com'
        from django.contrib.sites.models import Site
        self._orig_get_current = Site.objects.get_current
        Site.objects.get_current = lambda: DummySite()


    def test_localeurl_sitemap(self):
        sitemap = DummySitemap('fr')
        self.assertEqual(sitemap.get_urls()[0]['location'],
                         'http://www.example.com/fr/dummy/0/')


    def tearDown(self):
        super(SitemapTestCase, self).tearDown()
        from django.contrib.sites.models import Site
        Site.objects.get_current = self._orig_get_current



class ReverseTestCase(LocaleurlTestCase):
    def test_args_kwargs_none(self):
        url = reverse("dummy0", args=None, kwargs=None)
        self.assertEqual(url, "/en/dummy/")


    def test_args_none(self):
        url = reverse("dummy1", args=None, kwargs=dict(test="test"))
        self.assertEqual(url, "/en/dummy/test")


    def test_kwargs_none(self):
        url = reverse("dummy1", args=["test"], kwargs=None)
        self.assertEqual(url, "/en/dummy/test")
