"""
Test utilities.

"""

from django.conf import settings as django_settings
from django.core.handlers.wsgi import WSGIRequest
from django import template
from django.test import Client
from django.utils import encoding


NO_SETTING = object()

class TestSettingsManager(object):
    """
    A class which can modify some Django settings temporarily for a
    test and then revert them to their original values later.

    Based on the work by 'carljm':
    http://www.djangosnippets.org/snippets/1011/
    """
    def __init__(self, settings=django_settings):
        self._settings = settings
        self._original_settings = {}


    def set(self, **kwargs):
        self.set_from_dict(kwargs)


    def set_from_dict(self, settings):
        for k,v in settings.iteritems():
            self._original_settings.setdefault(k,
                    getattr(self._settings, k, NO_SETTING))
            setattr(self._settings, k, v)


    def revert(self):
        for k,v in self._original_settings.iteritems():
            if v == NO_SETTING:
                try:
                    delattr(self._settings, k)
                except AttributeError:
                    # Django < r11825
                    delattr(self._settings._wrapped, k)
            else:
                setattr(self._settings, k, v)
        self._original_settings = {}



class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.

    Usage:

    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})

    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client

    Once you have a request object you can pass it to any view function,
    just as if that view had been hooked up using a URLconf.

    Based on the work by Simon Willison:
    http://www.djangosnippets.org/snippets/963/
    """
    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)


class TestTemplate(template.Template):
    """
    TestTemplate behaves just like django.template.Template, but you can give
    it a list of template.Libraries to load before parsing the template. This
    is equivalent to adding a bunch of {% load %} tags to the beginning of your
    template string, but you can use custom tag libraries which do not belong
    to Django applications' templatetags packages.

    Based on the work by Alexander Khodyrev:
    http://www.djangosnippets.org/snippets/1641/
    """
    def __init__(self, template_string, name='<Unknown Template>',
            libraries=[]):
        try:
            template_string = encoding.smart_unicode(template_string)
        except UnicodeDecodeError:
            raise template.TemplateEncodingError(
                    "template content must be unicode or UTF-8 string")
        origin = template.StringOrigin(template_string)
        self.nodelist = self.my_compile_string(template_string, origin,
                libraries)
        self.name = name

    def my_compile_string(self, template_string, origin, libraries=[]):
        "Compiles template_string into NodeList ready for rendering"
        lexer = template.Lexer(template_string, origin)
        parser = template.Parser(lexer.tokenize())
        for lib in libraries:
            parser.add_library(lib)
        return parser.parse()
