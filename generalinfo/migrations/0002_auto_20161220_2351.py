# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generalinfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='higher',
            field=models.IntegerField(default=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='joint_discount',
            field=models.IntegerField(default=5),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='nat5',
            field=models.IntegerField(default=15),
            preserve_default=True,
        ),
    ]
