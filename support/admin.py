# -*- coding: utf-8 -*-
from django.contrib import admin
from support.models import *
from utils.admin import *
from django.utils.translation import ugettext_lazy as _

class SubjectCategoryTranslationInline(admin.StackedInline):
#    formfield_overrides = { models.CharField: {'widget': Textarea(attrs={'rows':'2','cols':'70'})},}
    model = SubjectCategoryTranslation

    save_on_top = True
    save_as = True
    extra = 3

class SubjectCategoryAdmin(admin.ModelAdmin):
        inlines = [SubjectCategoryTranslationInline,]

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
        list_display = ( 'editLink','category','creatation','status')
        list_filter = ['status', 'creatation','category']
        search_fields = ['subject','body']
        list_per_page=20


class MesajAdmin(admin.ModelAdmin):
    list_display = ('safe', 'fullname', 'subject', 'submit_time','email', 'called',  'archived' )
    list_display_links = ('fullname',)
    list_filter=('called', 'archived','safe')
    date_hierarchy = 'submit_time'
    search_fields = ['first_name','subject', 'message']
    readonly_fields = ('safe',)
    fieldsets = (

        (_(u'Content safety'), {
            'fields': ('safe', )
        }),
    (u'Personal Information', {
        'fields': ('first_name', 'email', 'phone', )
    }),
    (u'Message', {
        'fields': ('subject', 'message', )
    }),
    (u'Team', {
        'fields': ('called', 'notes', 'archived')
    }),
    )

admin_register(admin, namespace=globals())

