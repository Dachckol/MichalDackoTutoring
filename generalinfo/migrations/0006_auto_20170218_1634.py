# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generalinfo', '0005_profile_skype_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='higher',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='joint_discount',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nat5',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skype_discount',
            field=models.FloatField(max_length=5),
        ),
    ]
