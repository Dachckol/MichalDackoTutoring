# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generalinfo', '0004_auto_20161221_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='skype_discount',
            field=models.CharField(default=2, max_length=5),
            preserve_default=False,
        ),
    ]
