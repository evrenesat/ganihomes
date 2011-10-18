__author__ = 'Evren Esat Ozkan'

from django.contrib import admin
from utils.admin import admin_register
from models import *


#class TagInline(admin.TabularInline):
#    model = Tag

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'active', 'size')
    search_fields = ['title', ]
    list_filter = ['type', 'space', 'bedroom', ]
    save_on_top = True

    raw_id_fields=('owner', )
    #readonly_fields=['',]
    #save_as=True
    #ordering = ['',]
    #description=''
    #list_per_page=20
    #prepopulated_fields = {"slug": ("title",)}
#    inlines = [TagInline,]
    #list_display_links = ('','')
    #date_hierarchy = ''
    #list_select_related=False


    #def save_model(self, request, obj, form, change):
    #    obj.save()




admin_register(admin, namespace=globals())
