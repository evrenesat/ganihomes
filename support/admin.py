from django.contrib import admin
from support.models import *
from utils.admin import *

class SubjectCategoryAdmin(admin.ModelAdmin):
        pass

class TicketAdmin(admin.ModelAdmin):
        #prepopulated_fields = {"slug": ("title",)}
        #raw_id_fields=('', )
        #prepopulated_fields = {"slug": ("",)}
        #inlines = [,]
        save_on_top=True
        #list_display = ('','')
        #description=''
        #list_display_links = ('','')
        #list_filter = ['', '']
        #date_hierarchy = ''
        #search_fields = ['','']
        #ordering = ['','']
        #list_per_page=20
        #list_select_related=False
        list_display = ('editLink', 'username','category','creatation','status')
        list_filter = ['status', 'creatation','category']
        search_fields = ['subject','body']
        list_per_page=20


admin_register(admin, namespace=globals())

