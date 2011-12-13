from django import template
from django.template import Node, Token, TemplateSyntaxError
from django.template import resolve_variable, defaulttags
from django.template.defaultfilters import stringfilter
from django.utils.functional import wraps

from localeurl import utils

register = template.Library()



def chlocale(url, locale):
    """
    Changes the URL's locale prefix if the path is not locale-independent.
    Otherwise removes locale prefix.
    """
    _, path = utils.strip_script_prefix(url)
    _, path = utils.strip_path(path)
    return utils.locale_url(path, locale)


chlocale = stringfilter(chlocale)
register.filter('chlocale', chlocale)



def rmlocale(url):
    """Removes the locale prefix from the URL."""
    script_prefix, path = utils.strip_script_prefix(url)
    _, path = utils.strip_path(path)
    return ''.join([script_prefix, path])


rmlocale = stringfilter(rmlocale)
register.filter('rmlocale', rmlocale)



def locale_url(parser, token, django_url_tag):
    """
    Renders the url for the view with another locale prefix. The syntax is
    like the 'url' tag, only with a locale before the view.

    Examples:
      {% locale_url "de" cal.views.day day %}
      {% locale_url "nl" cal.views.home %}
      {% locale_url "en-gb" cal.views.month month as month_url %}
    """
    bits = token.split_contents()
    if len(bits) < 3:
        raise TemplateSyntaxError("'%s' takes at least two arguments:"
                " the locale and a view" % bits[0])
    urltoken = Token(token.token_type, bits[0] + ' ' + ' '.join(bits[2:]))
    urlnode = django_url_tag(parser, urltoken)
    return LocaleURLNode(bits[1], urlnode)


class LocaleURLNode(Node):
    def __init__(self, locale, urlnode):
        self.locale = locale
        self.urlnode = urlnode

    def render(self, context):
        locale = resolve_variable(self.locale, context)
        if utils.supported_language(locale) is None:
            raise ValueError("locale not in settings.LANGUAGES: %s" % locale)
        path = self.urlnode.render(context)
        if self.urlnode.asvar:
            self.urlnode.render(context)
            context[self.urlnode.asvar] = chlocale(context[self.urlnode.asvar],
                    locale)
            return ''
        else:
            return chlocale(path, locale)



def locale_url_wrapper(parser, token):
    return locale_url(parser, token, django_url_tag=defaulttags.url)


locale_url_wrapper = wraps(locale_url)(locale_url_wrapper)



register.tag('locale_url', locale_url_wrapper)
