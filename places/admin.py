__author__ = 'Evren Esat Ozkan'

from django.contrib import admin
from utils.admin import admin_register
from models import *


#class TagInline(admin.TabularInline):
#    model = Tag

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'active', 'size', 'timestamp','last_modified')
    search_fields = ['title', ]
    list_filter = ['type', 'space', 'bedroom', ]
    save_on_top = True

    raw_id_fields=('owner', )
    readonly_fields=['timestamp','last_modified']
    #save_as=True
    #ordering = ['',]
    #description=''
    #list_per_page=20
    prepopulated_fields = {"slug": ("title",)}
#    inlines = [TagInline,]
    #list_display_links = ('','')
    #date_hierarchy = ''
    #list_select_related=False


    #def save_model(self, request, obj, form, change):
    #    obj.save()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'category')
    search_fields = ['name', ]
    list_filter = ['category', ]
    save_on_top = True


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'type','reciver_type','sender_type' ,'active', 'timestamp')
#    search_fields = ['', ]
    list_filter = ['reciver_type','sender_type','active' ]
    save_on_top = True



admin_register(admin, namespace=globals())
