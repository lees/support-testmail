# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 12:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_auto_20160613_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
