from django import template
from django.templatetags.future import url
from django.utils.functional import wraps

from localeurl_tags import locale_url


register = template.Library()


def locale_url_wrapper(parser, token):
    return locale_url(parser, token, django_url_tag=url)


locale_url_wrapper = wraps(locale_url)(locale_url_wrapper)



register.tag('locale_url', locale_url_wrapper)
