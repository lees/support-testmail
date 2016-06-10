# -*- coding: utf-8 -*-

from django.db import models

class Request(models.Model):
    subject = models.CharField(max_length=255)
    creation_date = models.DateTimeField(u'Дата создания')
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True)
    author_email = models.EmailField()
    solved = models.BooleanField(default = False)
    solved_date = models.DateTimeField(u'Дата закрытия', blank=True)
    solved_by = models.CharField(max_length=255, blank=True)
    response_text = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #todo reverse
        return "/issue/%i/" % self.id
