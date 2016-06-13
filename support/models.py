# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Issue(models.Model):
    subject = models.CharField(max_length=255)
    creation_date = models.DateTimeField(u'Дата создания',auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey(User, related_name='issue_author', blank=True, null=True)
    author_email = models.EmailField(blank=True)
    solved = models.BooleanField(default = False)
    solved_date = models.DateTimeField(null=True, blank=True)
    solved_by = models.ForeignKey(User, related_name='issue_solved_by', null=True)
    response_text = models.TextField(blank=True)

    def clean(self):
        if self.author:
            return
        if self.author_email:
            return
        raise ValidationError('Должен быть заполнен автор обращения или адрес для уведомления')

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        # reverse приводит к циклическому импорту
        return "/issue/%s" % self.id
