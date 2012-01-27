# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
# Create your models here.
#from kup.middleware.threadlocals import get_current_user
#from books.models import lng
from places.countries import COUNTRIES
from places.options import INFORM_TYPES

class SubjectCategory(models.Model):
    """
    Classifications
    """
    name = models.CharField(_(u"Name"), max_length=200, null=True,  blank=True )
    hidden= models.BooleanField(_(u"Hidden"), default=False, help_text=_(u"Do not show this category.") )

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
      verbose_name = _(u'Subject Category')
      verbose_name_plural = _(u'Subject Categories')
      ordering=['name']

STATUS=((10,_(u'Waiting Reply')),(20,_(u'Replied')),(30,_(u'On going request')),(40,_(u'Closed')))
class Ticket(models.Model):


   category= models.ForeignKey(SubjectCategory, verbose_name=_(u"Subject Category"))
   status = models.SmallIntegerField(_(u'Status'),choices=STATUS,default=10)
   subject= models.CharField(_(u'Subject'),max_length=100)
   body= models.TextField(_(u'Body'))
   creatation= models.DateTimeField(_(u'Creatation'),auto_now_add=True)
   user = models.ForeignKey(User)
   #admin_url='/admin/support/mesaj/?durum__lt=40'

   def __unicode__(self):
      return self.subject

   def username(self):
      return self.user.get_profile()

   def get_absolute_url(self):
      return reverse('support_show_ticket', args=(self.id, ))
   #get_absolute_url = permalink(get_absolute_url)


#
#   def editLink(self):
#        return "<a href='%s'>%s</a>" % (reverse('support_admin_show_ticket', args=(self.id, )) ,  self.subject)
#   editLink.short_description = _(u'Show Ticket')
#   editLink.allow_tags=True

   class Meta:
      verbose_name = _(u'Support Ticket')
      verbose_name_plural = _(u'Support Tickets')
      get_latest_by = 'creatation'
      ordering=['status','creatation']


#from datetime import datetime

class Reply(models.Model):
   user = models.ForeignKey(User)
   body= models.TextField(_(u'Body'))
   creatation = models.DateTimeField(_(u'Creatation'),auto_now_add=True)
   ticket = models.ForeignKey(Ticket)

   def __unicode__(self):
      return u' '.join(self.body.split()[:5])

   class Meta:
      verbose_name = _(u'Ticket Reply')
      verbose_name_plural = _(u'Ticket Replies')
      get_latest_by = 'creatation'



class Inform(models.Model):
    '''customer is an informer'''
    title = models.CharField(_('Title'), max_length=30)
    user = models.ForeignKey(User,verbose_name=_('Sender'))
    type = models.SmallIntegerField(_('Type'), choices=INFORM_TYPES)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    text = models.TextField(_('Details'), null=True, blank=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.title,)


class Mesaj(models.Model):
    first_name = models.CharField(_(u"First Name"), max_length=50)
    last_name = models.CharField(_(u"Last Name"), max_length=50, default='')
    country=models.SmallIntegerField(_(u"Country"), default=0, choices=COUNTRIES)
    email = models.EmailField(_(u"Email"))
    phone = models.CharField(_(u"Phone"), max_length=30, default="")
    subject= models.CharField(_(u"Subject"), max_length=200, default='')
    message = models.TextField(_(u"Message"))
    submit_time = models.DateTimeField(_(u"Form Submit Time"), auto_now_add=True)
    called= models.BooleanField(_(u"Called Back?"), default=False)
    archived= models.BooleanField(_(u"Archived"), default=False)
    notes = models.TextField(_(u"Notes"), null=True,  blank=True )

    def get_absolute_url(self):
        '/admin/support/message/%s' % self.id

    def fullname(self):
        return u'%s %s' % (self.first_name, self.last_name)
    fullname.short_description = _(u'Name')

    def __unicode__(self):
        return self.fullname()


    class Meta:
        verbose_name = _(u"Contact Us Record")
        verbose_name_plural = _(u"Contact Us Records")
        ordering = ['-submit_time', ]
        get_latest_by='submit_time'
        #order_with_respect_to = ''
        #unique_together = (("", ""),)
        #permissions = (("can_do_something", "Can do something"),)
