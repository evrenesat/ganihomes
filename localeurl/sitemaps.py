from django.contrib.sitemaps import Sitemap

from localeurl.templatetags.localeurl_tags import chlocale

class LocaleurlSitemap(Sitemap):
    """
    From a `snippet by tomas`_.

    .. _`snippet by tomas`: http://www.djangosnippets.org/snippets/1620/
    """
    def __init__(self, language):
        self.language = language
        
    def location(self, obj):
        return chlocale(obj.get_absolute_url(), self.language)
