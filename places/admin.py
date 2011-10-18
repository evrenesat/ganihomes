__author__ = 'Evren Esat Ozkan'

from django.contrib import admin
from utils.admin import admin_register
from models import *


class PhotoInline(admin.TabularInline):
    model = Photo


class BookingAdmin(admin.ModelAdmin):
    list_display = ('host', 'guest', 'place', 'valid', 'status')
    search_fields = ['summary', ]
    list_filter = ['status','valid', ]
    save_on_top = True


class ReservedDatesAdmin(admin.ModelAdmin):
    list_display = ('', '')
    search_fields = ['', ]
    list_filter = ['', ]
    save_on_top = True



class BookingInline(admin.TabularInline):
    model = Booking


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
    inlines = [PhotoInline,BookingInline]
    #list_display_links = ('','')
    #date_hierarchy = ''
    #list_select_related=False


    #def save_model(self, request, obj, form, change):
    #    obj.save()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'category')
    search_fields = ['name', ]
    list_filter = ['category', ]


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'main', 'active')
    search_fields = ['name','code' ]
    list_filter = ['active', ]


class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ['active', ]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('usr', )
#    search_fields = ['', ]
#    list_filter = ['', ]

    save_on_top = True



class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'type','reciver_type','sender_type' ,'active', 'timestamp')
#    search_fields = ['', ]
    list_filter = ['reciver_type','sender_type','active' ]
    save_on_top = True




admin_register(admin, namespace=globals())
