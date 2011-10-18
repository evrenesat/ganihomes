# -*- coding: utf-8 -*-
# Create your views here.

from support.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.forms import widgets
from django.shortcuts import render_to_response,get_object_or_404
from utils.mail2perm import mail2perm
from django.core.mail import send_mail
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from utils.htmlmail import htmlmail
#send_mail(sbj,msg,sender,recips)
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.sites.models import Site

#domain=Site.objects.filter(pk=1).values('domain')[0]['domain']


try:
    domain=Site.objects.all().values('domain')[0]['domain']
except:
    domain=''

class TicketForm(forms.ModelForm):
    body= forms.CharField(widget=forms.Textarea(attrs={'cols': '70', 'rows': '8'}), label=_(u'Destek Mesajı'))
    subject=forms.CharField(widget=forms.TextInput(attrs={'size':'70'}), label=_(u'Konu'))
#    tip = forms.ChoiceField(label='Değerlendirme',  choices=Mesaj.TIP)
    category= forms.ModelChoiceField(queryset=SubjectCategory.objects.exclude(hidden=True), label=_(u'Kategori'))
    class Meta:
        model=Ticket
        exclude = ('user','status')

@login_required
def Post(request):
   if request.POST:
      form = TicketForm(request.POST)
      if form.is_valid():
         obj=form.save(commit=False)
         obj.status=10
         obj.user=request.user
         obj.save()
         mail2perm(obj,url=reverse('support_admin_show_ticket', args=(obj.id, )))
         return HttpResponseRedirect(reverse('support_thanks'))
   else:
      form = TicketForm()
      form.fields['subject'].initial=request.GET.get('subject', '')
      form.fields['category'].initial=int(request.GET.get('category', 0))
   return render_to_response('support/form.html', {'form': form, 'title':_(u'Müşteri Destek Sistemi'),}, context_instance=RequestContext(request, {}))

@login_required
def List(request):
   messageList=Ticket.objects.select_related().filter(user=request.user)
   li=[]
   for l in messageList:
      try: last_reply=l.reply_set.all()[0].creatation
      except:last_reply=''
      li.append({ 'subject':l.subject, 'status':l.get_status_display(), 'last_reply':last_reply, 'id':l.id, 'url':l.get_absolute_url() })
   return render_to_response('support/list.html', {'li': li, 'title':_(u'Müşteri Destek Sistemi'),}, context_instance=RequestContext(request, {}))

#@staff_member_required
@permission_required('support.delete_ticket')
def AdminClose(request, id=None):
   if id is None: id=request.GET.get('id')
   ticket=get_object_or_404(Ticket,pk=id)
   ticket.status=40
   ticket.save()
   request.user.message_set.create(message=ugettext(u'Ticket closed.'))
   return HttpResponseRedirect('/admin/support/ticket')

#@staff_member_required
@permission_required('destek.add_ticket')
def AdminShow(request,id):
   return Show(request,id, is_admin=True)

class ReplyForm(forms.ModelForm):
    body= forms.CharField(widget=forms.Textarea(attrs={'cols': '50', 'rows': '8'}), label=_(u'Destek Mesajı'),)
    class Meta:
        model=Reply
        exclude = ('user','ticket')


@login_required
def Show(request,id=None, is_admin=False):
   if id is None: id=request.GET.get('id',request.session.get('ticket_id'))
   request.session['ticket_id']=id
   if is_admin:
      ticket=get_object_or_404(Ticket,pk=id)
      status=20
      temple='support/admin/show.html'
      redir='/admin/support/ticket/?status__lt=40'
   else:
      redir=reverse('support_thanks')
      temple='support/show.html'
      status=30
      ticket=get_object_or_404(Ticket,user=request.user,pk=id)
#   kullanici = UserProfile.objects.get(user=mesaj.kullanici)
   if request.POST:
      form = ReplyForm(request.POST)
      if form.is_valid():
         obj=form.save(commit=False)
         ticket.status=status
         ticket.save()
         request.user.message_set.create(message=ugettext(u'Mesajınız başarılı bir şekilde alındı.'))
         obj.user=request.user
         obj.ticket=ticket
         obj.save()
#         if request.user.is_staff:
#             htmlmail('Destek sorunuza cevap verildi', ticket.user.email, {'ticket':ticket,'domain':domain,'url':ticket.get_absolute_url()}, 'support/ticket_replied_body.html', )
#         else:
         mail2perm(obj,url=reverse('support_admin_show_ticket', args=(ticket.id, )) )
         return HttpResponseRedirect(redir)
   else:
      form = ReplyForm()
   return render_to_response(temple,{
   'open':ticket.status<40,
   'title':_(u'Müşteri Destek Sistemi'),
   'form': form,
   'm':ticket,
   'replies':ticket.reply_set.order_by('creatation')
   },
   context_instance=RequestContext(request, {}))

