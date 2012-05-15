# Based on http://djangosnippets.org/snippets/285/
# Sending html emails with images attached in Django

# download and install BeautifulSoup from http://www.crummy.com/software/BeautifulSoup/
from BeautifulSoup import BeautifulSoup

from django.conf import settings
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives

from email.MIMEImage import MIMEImage
import email.Charset

CHARSET = 'utf-8'

email.Charset.add_charset(CHARSET, email.Charset.SHORTEST, None, None)

named = lambda email, name: ('%s <%s>' % (name, email)) if name else email

def image_finder(tag):
    return (tag.name == u'img' or
            tag.name == u'table' and tag.has_key('background'))

def render(context, template):
    if template:
        t = loader.get_template(template)
        return t.render(Context(context))
    return context

def send_html_mail(subject, recipient, message, template='',
                   recipient_name='', sender_name='', sender=None,
                   CHARSET=CHARSET):
    html = render(message, template)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=html,
        to=[named(recipient, recipient_name)],
        from_email=named(sender, sender_name),
    )
    msg.content_subtype = "html"
    msg.send()
