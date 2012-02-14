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
    """
    If you want to use Django template system:
       use `message` and define `template`.

    If you want to use images in html message, no problem,
    it will attach automatically found files in html template.
    (image paths are relative to PROJECT_PATH)
    """

    html = render(message, template)

#    # Image processing, replace the current image urls with attached images.
#    soup = BeautifulSoup(html)
#    images = []
#    added_images = []
#    for index, tag in enumerate(soup.findAll(image_finder)):
#        if tag.name == u'img':
#            name = 'src'
#        elif tag.name == u'table':
#            name = 'background'
#        # If the image was already added, skip it.
#        if tag[name] in added_images:
#            continue
#        added_images.append(tag[name])
#        images.append((tag[name], 'img%d' % index))
#        tag[name] = 'cid:img%d' % index
#    html = str(soup)


    msg = EmailMultiAlternatives(
        subject=subject,
        body=html,
        to=[named(recipient, recipient_name)],
        from_email=named(sender, sender_name),
    )

#    for filename, file_id in images:
#        image_file = open(settings.STATIC_ROOT + filename, 'rb')
#        msg_image = MIMEImage(image_file.read())
#        image_file.close()
#        msg_image.add_header('Content-ID', '<%s>' % file_id)
#        msg.attach(msg_image)

    msg.content_subtype = "html"
    msg.send()
