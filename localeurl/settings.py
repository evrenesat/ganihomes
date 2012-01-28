# -*- coding: utf-8 -*-
import re
from django.conf import settings

#def get_enabled_locales():
#    locales = []
#    try:
#        import dbsettings
#        for l in dbsettings.ghs.enabled_langs.split('\n'):
#            locales.append(l.split(','))
#        return locales
#    except:
#        return [('en','English'),('tr','Türkçe')]
#


SUPPORTED_LOCALES = dict(settings.ENABLED_LOCALES)
# Issue #15. Sort locale codes to avoid matching e.g. 'pt' before 'pt-br'
LOCALES_RE = '|'.join(
    sorted(SUPPORTED_LOCALES.keys(), key=lambda i: len(i), reverse=True))
PATH_RE = re.compile(r'^/(?P<locale>%s)(?P<path>.*)$' % LOCALES_RE)


LOCALE_INDEPENDENT_PATHS = [re.compile(p) for p in
                            getattr(settings, 'LOCALE_INDEPENDENT_PATHS', [
                                r'^/upload_photo/',
                                r'^/dashboard/pfoto/',
                                r'^/jsearch',
                                r'^/facebook/connect',
                                r'^/delete_photo',
                                r'^/bookmark',
#                                r'nolocale=1$'
                            ])]

LOCALE_INDEPENDENT_MEDIA_URL = getattr(settings,
        'LOCALE_INDEPENDENT_MEDIA_URL', True)

LOCALE_INDEPENDENT_STATIC_URL = getattr(settings,
        'LOCALE_INDEPENDENT_STATIC_URL', True)

PREFIX_DEFAULT_LOCALE = getattr(settings, 'PREFIX_DEFAULT_LOCALE', True)

USE_ACCEPT_LANGUAGE = getattr(settings, 'LOCALEURL_USE_ACCEPT_LANGUAGE', True)

LOCALE_REDIRECT_PERMANENT = getattr(settings, 'LOCALE_REDIRECT_PERMANENT', False)
