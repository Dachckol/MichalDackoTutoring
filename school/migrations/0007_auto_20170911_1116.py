# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_auto_20170910_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='about',
            field=models.TextField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='picturelink',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='qualifications',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
