# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generalinfo', '0003_auto_20161220_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='higher',
            field=models.CharField(max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='joint_discount',
            field=models.CharField(max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='nat5',
            field=models.CharField(max_length=5),
            preserve_default=True,
        ),
    ]
