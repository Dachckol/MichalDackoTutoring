# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=40)),
                ('level', models.CharField(max_length=10)),
                ('details', models.TextField(blank=True)),
                ('time', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('priority', models.IntegerField(default=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
