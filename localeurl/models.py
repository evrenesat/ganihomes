from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
from localeurl import utils

def reverse(*args, **kwargs):
    reverse_kwargs = kwargs.get('kwargs') or {}
    locale = utils.supported_language(reverse_kwargs.pop(
            'locale', translation.get_language()))
    url = django_reverse(*args, **kwargs)
    _, path = utils.strip_script_prefix(url)
    return utils.locale_url(path, locale)

django_reverse = None

def patch_reverse():
    """
    Monkey-patches the urlresolvers.reverse function. Will not patch twice.
    """
    global django_reverse
    if urlresolvers.reverse is not reverse:
        django_reverse = urlresolvers.reverse
        urlresolvers.reverse = reverse

if settings.USE_I18N:
    patch_reverse()
