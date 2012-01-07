# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
#import logging
#log = logging.getLogger('genel')
from utils.cache import kes

class Category(models.Model):
    """Tag category"""

    text = models.CharField(_('Name'), max_length=100)
#    lang = models.CharField(_('Category'), max_length=2, db_index=True, choices=settings.LANGUAGES)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Category')
        verbose_name_plural = _('FAQ Categories')

    def __unicode__(self):
        return '%s' % (self.text,)

class CategoryTranslation(models.Model):
    """Place description"""

    category = models.ForeignKey('Category')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Translation'), max_length=100)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Category Name Translation')
        verbose_name_plural = _('FAQ Category Name Translations')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.category_id, self.lang)

from collections import defaultdict
class Question(models.Model):
    """Place tags"""

    category = models.ForeignKey('Category')
#    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    order = models.SmallIntegerField(_('Order'),default=100)
    text = models.CharField(_('Question'), max_length=250)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    @classmethod
    def getFaqs(cls, lang):
        return kes(lang,'faqs').g({}) or cls._updateCache(lang)

    def getTrans(self,lang):
        return self.questiontranslation_set.filter(lang=lang).values_list('text',flat=True)[0]

    @classmethod
    def _updateCache(cls, lang=None):
        for code,name in settings.LANGUAGES:
            di = defaultdict(list)
            cat_names = dict(CategoryTranslation.objects.filter(lang=code).values_list('category_id','text'))
            for a in Answer.objects.select_related().order_by('question__order').filter(lang=code, active=True):
                di[cat_names.get(a.question.category_id,'---')].append({'answer':mark_safe(a.text), 'qid':a.question_id, 'question':a.question.getTrans(code)})
            di = di.items()
            kes(code,'faqs').s(di,99)
            if lang == code:
                lang = di
        return lang


    def save(self, *args, **kwargs):
        self._updateCache()
        super(Question, self).save(*args, **kwargs)

    class Meta:
        app_label = 'website'
        ordering = ['order']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Question')
        verbose_name_plural = _('FAQ Questions')

    def __unicode__(self):
        return '%s' % (self.text,)


class QuestionTranslation(models.Model):
    """Place description"""

    question = models.ForeignKey('Question')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Question'), max_length=250)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Question Translation')
        verbose_name_plural = _('FAQ Question Translations')

    def __unicode__(self):
        return '#%s Lang:%s' % (self.question_id, self.lang)

class Answer(models.Model):
    """Place tags"""

    question = models.ForeignKey('Question')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.TextField(_('Answer'))
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Answer')
        verbose_name_plural = _('FAQ Answers')

    def __unicode__(self):
        return '%s' % (self.text,)

    def save(self, *args, **kwargs):
        self.question._updateCache()
        super(Answer, self).save(*args, **kwargs)
