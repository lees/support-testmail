# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-11 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='solved_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
