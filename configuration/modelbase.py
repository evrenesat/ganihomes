# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

CACHE_PREFIX = 'config_'

class ConfigBase(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('Configuration Options')
        verbose_name_plural = _('Configuration Options')

    def save(self, *args, **kwargs):
        for key,val in self.__dict__.items():
            if not key == '_state':
                cache.set(CACHE_PREFIX + key, val)
        super(ConfigBase, self).save(*args, **kwargs)

    @classmethod
    def getValue(cls, name):
        try:
            val = cls.objects.values_list(name, flat=True)[0]
        except IndexError:
            val = cls._meta.get_field_by_name(name)[0].default
#            if isinstance(default_val, models.NOT_PROVIDED):
#               return val
        cache.set(CACHE_PREFIX + name, val)
        return val

    @classmethod
    def setValue(cls, name, val):
        obj = cls.objects.all()[0]
        setattr(obj, name, val)
        obj.save()
        cache.get(CACHE_PREFIX + name, val)
        return val

    @classmethod
    def __call__(cls, key):
        return  ( cache.get(CACHE_PREFIX + key) or cls.getValue(key))

    def __unicode__(self):
        return force_unicode(_(u'Configuration Options'))
