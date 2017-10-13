# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generalinfo', '0002_auto_20161220_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='higher',
            field=models.FloatField(default=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='joint_discount',
            field=models.FloatField(default=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='nat5',
            field=models.FloatField(default=15),
            preserve_default=True,
        ),
    ]
