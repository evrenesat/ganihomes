# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.sites.models import Site
from django.core.mail import send_mail
import logging
log = logging.getLogger('genel')

domain=Site.objects.filter(pk=1).values('domain')[0]['domain']

def mail2perm(obj, url='', pre=None, msg=None, perm='change', sender=settings.EMAIL_HOST_USER, sbj=None):
   if not msg:
      if not url:
         try: url=obj.get_absolute_url()
         except: pass
      if url:url=u'\n\nDetayları görmek için linke tıklayın:\n\n http://%s%s' % (domain,url)
      msg='%s%s'  % ( (pre or sbj) , url )

   codename = '%s_%s' % (perm, obj._meta.module_name)
   perm=Permission.objects.filter(codename=codename, content_type__app_label=obj._meta.app_label).get()

   recips=[]
   for user in perm.user_set.all():
      if user.email: recips.append(user.email)

   try:
       send_mail((sbj or 'Yeni %s'% obj._meta.verbose_name.title()), msg, sender, recips)
   except:
       log.exception('eposta gonderilemedi')



#import smtplib
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email.MIMEText import MIMEText
#from email import Encoders
#import os
#from django.conf import settings
#from django.contrib.sites.models import Site
#from django.contrib.auth.models import Permission
#
#gmail_user = settings.EMAIL_HOST_USER
#gmail_pwd = settings.EMAIL_HOST_PASSWORD
#gmail_smtp = settings.EMAIL_HOST
#gmail_smtp_port = settings.EMAIL_PORT
#
#def mail(to, subject, text, attach):
#   msg = MIMEMultipart()
#
#   msg['From'] = gmail_user
#   msg['To'] = to
#   msg['Subject'] = subject
#
#   assert False,  to
#
#   msg.attach(MIMEText(text))
#
#   part = MIMEBase('application', 'octet-stream')
#   part.set_payload(open(attach, 'rb').read())
#   Encoders.encode_base64(part)
#   part.add_header('Content-Disposition',
#           'attachment; filename="%s"' % os.path.basename(attach))
#   msg.attach(part)
#
#   mailServer = smtplib.SMTP(gmail_smtp, gmail_smtp_port)
#   mailServer.ehlo()
#   mailServer.starttls()
#   mailServer.ehlo()
#   mailServer.login(gmail_user, gmail_pwd)
#
#   mailServer.sendmail(gmail_user, to, msg.as_string())
#   # Should be mailServer.quit(), but that crashes...
#   mailServer.close()
#
#"""
#mail("some.person@some.address.com",
#   "Hello from python!",
#   "This is a email sent with python",
#   "my_picture.jpg")
#"""
#
#domain=Site.objects.filter(pk=1).values('domain')[0]['domain']
#
#def mail2perm(obj, url='', pre=None, msg=None, perm='change', sender=settings.DEFAULT_FROM_EMAIL, sbj=None):
#   if not msg:
#      if not url:
#         try: url=obj.get_absolute_url()
#         except: pass
#      if url:url=u'\n\nDetayları görmek için linke tıklayın:\n\n http://%s%s' % (domain,url)
#      msg='%s%s'  % ( (pre or sbj) , url )
#
#   perm=Permission.objects.filter(codename='%s_%s'%(perm,obj._meta.module_name), content_type__app_label=obj._meta.app_label).get()
#
#   recips=[]
#   for user in perm.user_set.all():
#      if user.email: recips.append(user.email)
#
#   assert False, recips
#   try: mail(recips, (sbj or 'Yeni %s'% obj._meta.verbose_name.title()), msg,  attach=None)
#   except: pass
