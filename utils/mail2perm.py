# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.sites.models import Site
from django.core.mail import send_mail
import logging
log = logging.getLogger('genel')



def mail2perm(obj, url='', pre=None, msg=None, perm='change', sender=settings.DEFAULT_FROM_EMAIL, sbj=None):
   if not msg:
      domain=Site.objects.filter(pk=1).values('domain')[0]['domain']
      if not url:
         try: url=obj.get_absolute_url()
         except: pass
      if url:
          url=u'\n\nDetayları görmek için linke tıklayın:\n\n http://%s%s' % (domain,url)
      msg='%s%s'  % ( (pre or sbj) , url )

   codename = '%s_%s' % (perm, obj._meta.module_name)
   perm=Permission.objects.filter(codename=codename, content_type__app_label=obj._meta.app_label).get()

   recips=[]
#   log.info('perm for obj : %s %s'% (obj, perm))
   for user in perm.user_set.all():
      if user.email: recips.append(user.email)
#   log.info('recips : %s'% recips)

   try:
       send_mail((sbj or 'Yeni %s'% obj._meta.verbose_name.title()), msg, sender, recips)
   except:
       log.exception('eposta gonderilemedi')


