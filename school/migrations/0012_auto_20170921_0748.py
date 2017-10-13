# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_auto_20170918_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='uploads',
            field=models.ManyToManyField(blank=True, related_name='Sessions', to='school.Upload'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='data',
            field=models.FileField(upload_to='uploads/2017/9'),
        ),
    ]