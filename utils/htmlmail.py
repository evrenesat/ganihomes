# -*- coding: utf-8 -*-

# Sending html emails in Django
# Report any bugs to esat @t sleytr*net
# snippet url: http://sleytr.net/Sending+html+email+in+Django
# Evren Esat Ozkan
# v0.1

#download and install feedparser from http://feedparser.org
#download and install StripOGram from http://www.zope.org/Members/chrisw/StripOGram
from utils.feedparser import _sanitizeHTML
from utils.stripogram import html2text


from django.conf import settings
from django.template import loader, Context

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from smtplib import SMTP
import email.Charset

from django.core.mail import send_mail

###################### TEST EDIYORUZ
from email.Charset import Charset
from email.MIMEText import MIMEText as OriginalMIMEText
from email.MIMENonMultipart import MIMENonMultipart

class MTText(OriginalMIMEText):

    def __init__(self, _text, _subtype='plain', _charset='us-ascii'):
        if not isinstance(_charset,Charset):
            _charset = Charset(_charset)
        if isinstance(_text,unicode):
            _text = _text.encode(_charset.input_charset)
        MIMENonMultipart.__init__(self, 'text', _subtype, **{'charset': _charset.input_charset})
        self.set_payload(_text, _charset)

###################### TEST BITTI



charset='UTF-8'

#smtp_server='localhost'
#smtp_user=''
#smtp_pass=''
'''
smtp_server='207.000.000.000'
smtp_user='email@.com'
smtp_pass='password'
'''

email.Charset.add_charset( charset, email.Charset.SHORTEST, None, None )

def htmlmail(sbj,recip,msg,template=u'',texttemplate=u'',textmsg=u'',images=(), recip_name=u'',sender=settings.DEFAULT_FROM_EMAIL,sender_name=u'',charset=charset):
   '''
   if you want to use Django template system:
      use `msg` and optionally `textmsg` as template context (dict)
      and define `template` and optionally `texttemplate` variables.
   otherwise msg and textmsg variables are used as html and text message sources.

   if you want to use images in html message, define pyhsical paths and ids in tupels.
   src path is relative to  MEDIA_ROOT
   example:
   images=(('email_images/logo.gif','img1'),('email_images/footer.gif','img2'))
   and use them in html like this:
   <img src="cid:img1">
   ...
   <img src="cid:img2">
   '''
   html=render(msg,template)

   if texttemplate or textmsg: text=render((textmsg or msg),texttemplate)
   else: text= html2text(_sanitizeHTML(html,charset))

   # Create the root message and fill in the from, to, and subject headers
   msgRoot = MIMEMultipart('related')
#   msgRoot['Subject'] = sbj
#   msgRoot['From'] = named(sender,sender_name)
#   msgRoot['To'] =  named(recip,recip_name)
   msgRoot.preamble = 'This is a multi-part message in MIME format.'

   msgAlternative = MIMEMultipart('alternative')
   msgRoot.attach(msgAlternative)

   msgAlternative.attach(MTText(text, _charset=charset))
   msgAlternative.attach(MTText(html, 'html', _charset=charset))

   for img in images:
      fp = open(settings.MEDIA_ROOT+img[0], 'rb')

      msgImage = MIMEImage(fp.read())
      fp.close()
      msgImage.add_header('Content-ID', '<'+img[1]+'>')
      msgRoot.attach(msgImage)
   recip=[recip]
   send_mail(sbj, msgRoot.as_string(), sender, recip)
#   smtp = SMTP()
#   smtp.connect(smtp_server)
#   if smtp_user: smtp.login(smtp_user, smtp_pass)
#   smtp.sendmail(sender, recip, msgRoot.as_string())
#   smtp.quit()


def render(context,template):
   return template and loader.get_template(template).render(Context(context)) or context


#def render(context,template):
#   if template:
#      t = loader.get_template(template)
#      return t.render(Context(context))
#   return context

def named(mail,name):
   if name: return u'%s <%s>' % (name,mail)
   return mail

#htmlemail('deneme','sleytr@gmail.com',{'sirketadi':'ATLILAR A.Ş.','siparis':[]},'eposta/siparis_tamamlandi.html',images=(('son/images/logo-rozet.gif','image1'),),sender_name='Atlılar A.Ş.')
