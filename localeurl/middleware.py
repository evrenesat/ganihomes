from django.conf import settings
import django.core.exceptions
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils import translation
from django.utils.encoding import iri_to_uri
from django.utils.translation.trans_real import parse_accept_lang_header
from localeurl import settings as localeurl_settings
# Importing models ensures that reverse() is patched soon enough. Refs #5.
from localeurl import utils

# Make sure the default language is in the list of supported languages
assert utils.supported_language(settings.LANGUAGE_CODE) is not None, \
        "Please ensure that settings.LANGUAGE_CODE is in settings.LANGUAGES."

class LocaleURLMiddleware(object):
    """
    Middleware that sets the language based on the request path prefix and
    strips that prefix from the path. It will also automatically redirect any
    path without a prefix, unless PREFIX_DEFAULT_LOCALE is set to True.
    Exceptions are paths beginning with MEDIA_URL and/or STATIC_URL (if
    settings.LOCALE_INDEPENDENT_MEDIA_URL and/or
    settings.LOCALE_INDEPENDENT_STATIC_URL are set) or matching any regular
    expression from LOCALE_INDEPENDENT_PATHS from the project settings.

    For example, the path '/en/admin/' will set request.LANGUAGE_CODE to 'en'
    and request.path to '/admin/'.

    Alternatively, the language is set by the first component of the domain
    name. For example, a request on 'fr.example.com' would set the language to
    French.

    If you use this middleware the django.core.urlresolvers.reverse function
    is be patched to return paths with locale prefix (see models.py).
    """
    def __init__(self):
        if not settings.USE_I18N:
            raise django.core.exceptions.MiddlewareNotUsed()

    def process_request(self, request):
        locale, path = utils.strip_path(request.path_info)
        if localeurl_settings.USE_ACCEPT_LANGUAGE and not locale:
            accept_langs = filter(lambda x: x, [utils.supported_language(lang[0])
                                                for lang in
                                                parse_accept_lang_header(
                        request.META.get('HTTP_ACCEPT_LANGUAGE', ''))])
            if accept_langs:
                locale = accept_langs[0]
        locale_path = utils.locale_path(path, locale)
        if locale_path != request.path_info:
            if request.META.get("QUERY_STRING", ""):
                locale_path = "%s?%s" % (locale_path,
                        request.META['QUERY_STRING'])
            locale_url = utils.add_script_prefix(locale_path)
            redirect_class = HttpResponsePermanentRedirect
            if not localeurl_settings.LOCALE_REDIRECT_PERMANENT:
                redirect_class = HttpResponseRedirect
            # @@@ iri_to_uri for Django 1.0; 1.1+ do it in HttpResp...Redirect
            return redirect_class(iri_to_uri(locale_url))
        request.path_info = path
        if not locale:
            try:
                locale = request.LANGUAGE_CODE
            except AttributeError:
                locale = settings.LANGUAGE_CODE
        translation.activate(locale)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
