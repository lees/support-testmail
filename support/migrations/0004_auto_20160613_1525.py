# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 12:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_auto_20160611_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='solved_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_solved_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
