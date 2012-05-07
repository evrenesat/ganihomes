# -*- coding: utf-8 -*-
#from cms.utils.i18n import get_default_language
from django.conf import settings
from django.core.urlresolvers import reverse
from django.middleware.locale import LocaleMiddleware
from django.utils import translation
from website.models.dil import Dil
import re
import urllib

from configuration import configuration

HAS_LANG_PREFIX_RE = re.compile(r"^/(%s)/.*" % "|".join(map(lambda l: re.escape(l[0]), settings.LANGUAGES)))

def has_lang_prefix(path):
    check = HAS_LANG_PREFIX_RE.match(path)
    if check is not None:
        return check.group(1)
    else:
        return False

class MultilingualURLMiddleware:
    SUPPORTED = configuration('listed_langs').split('\n')
    def get_language_from_request (self,request):
        changed = False
        prefix = has_lang_prefix(request.path_info)
        if prefix:
            request.path = "/" + "/".join(request.path.split("/")[2:])
            request.path_info = "/" + "/".join(request.path_info.split("/")[2:])
            t = prefix
            if t in self.SUPPORTED:
                lang = t
                if hasattr(request, "session"):
                    request.session["django_language"] = lang
                changed = True
        else:
            lang = translation.get_language_from_request(request)
        if not changed:
            if hasattr(request, "session"):
                lang = request.session.get("django_language", None)
                if lang in self.SUPPORTED and lang is not None:
                    return lang
            elif "django_language" in request.COOKIES.keys():
                lang = request.COOKIES.get("django_language", None)
                if lang in self.SUPPORTED and lang is not None:
                    return lang
            if not lang:
                lang = translation.get_language_from_request(request)
        lang = 'tr'#get_default_language(lang)
        return lang

    def process_request(self, request):
        language = self.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = language

    def process_response(self, request, response):
        language = getattr(request, 'LANGUAGE_CODE', self.get_language_from_request(request))
        local_middleware = LocaleMiddleware()
        response =local_middleware.process_response(request, response)
        path = unicode(request.path)

        # note: pages_root is assumed to end in '/'.
        #       testing this and throwing an exception otherwise, would probably be a good idea

        if not path.startswith(settings.MEDIA_URL) and \
                not path.startswith(settings.ADMIN_MEDIA_PREFIX) and \
                response.status_code == 200 and \
                response._headers['content-type'][1].split(';')[0] == "text/html":
#            pages_root = urllib.unquote(reverse("pages-root"))
            try:
                decoded_response = response.content.decode('utf-8')
            except UnicodeDecodeError:
                decoded_response = response.content

#            response.content = patch_response(
#                decoded_response,
#                pages_root,
#                request.LANGUAGE_CODE
#            )

        if (response.status_code == 301 or response.status_code == 302 ):
            location = response['Location']
            if not has_lang_prefix(location) and location.startswith("/") and \
                    not location.startswith(settings.MEDIA_URL) and \
                    not location.startswith(settings.ADMIN_MEDIA_PREFIX):
                response['Location'] = "/%s%s" % (language, location)
        response.set_cookie("django_language", language)
        return response
