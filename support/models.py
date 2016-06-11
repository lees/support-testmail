# -*- coding: utf-8 -*-

from django.db import models

class Issue(models.Model):
    subject = models.CharField(max_length=255)
    creation_date = models.DateTimeField(u'Дата создания')
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True)
    author_email = models.EmailField()
    solved = models.BooleanField(default = False)
    solved_date = models.DateTimeField(null=True, blank=True)
    solved_by = models.CharField(max_length=255, blank=True)
    response_text = models.TextField(blank=True)

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        # reverse приводит к циклическому импорту
        return "/issue/%s" % self.id
