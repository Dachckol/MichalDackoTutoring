# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='level',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='subject',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='time',
            field=models.CharField(max_length=50),
        ),
    ]
