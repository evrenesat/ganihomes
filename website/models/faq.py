# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
#import logging
#log = logging.getLogger('genel')

class Category(models.Model):
    """Tag category"""

    text = models.CharField(_('Name'), max_length=100)
    lang = models.CharField(_('Category'), max_length=2, db_index=True, choices=settings.LANGUAGES)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Tag Category')
        verbose_name_plural = _('Tag Categories')

    def __unicode__(self):
        return '%s' % (self.text,)

class CategoryTranslation(models.Model):
    """Place description"""

    category = models.ForeignKey('Category')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Translation'), max_length=100)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Category Name Translation')
        verbose_name_plural = _('Category Name Translations')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.category_id, self.lang)


class Question(models.Model):
    """Place tags"""

    category = models.ForeignKey('Category')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Question'), max_length=250)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __unicode__(self):
        return '%s' % (self.text,)


class QuestionTranslation(models.Model):
    """Place description"""

    question = models.ForeignKey('Question')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Question'), max_length=250)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Tag Translation')
        verbose_name_plural = _('Tag Translations')

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
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __unicode__(self):
        return '%s' % (self.text,)


class AnswerTranslation(models.Model):
    """Place description"""

    answer = models.ForeignKey('Answer')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.TextField(_('Answer'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Answer Translation')
        verbose_name_plural = _('Answer Translations')

    def __unicode__(self):
        return '#%s Lang:%s' % (self.answer_id, self.lang)
