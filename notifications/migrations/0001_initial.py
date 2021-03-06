# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('hasLink', models.BooleanField(default=False)),
                ('link', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=50)),
                ('css', models.CharField(max_length=10)),
                ('expired', models.BooleanField(default=False)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='school.Profile')),
            ],
        ),
    ]
