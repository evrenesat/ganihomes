# -*- coding: utf-8 -*-

from django.contrib import admin
#from django.forms import Textarea
from models import Config


class ConfigAdmin(admin.ModelAdmin):
    save_on_top = True

    def has_add_permission(self, request):
        return False if Config.objects.count() \
                    else super(ConfigAdmin, self).has_add_permission(request)



admin.site.register(Config, ConfigAdmin)

