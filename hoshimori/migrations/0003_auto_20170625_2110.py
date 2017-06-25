# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hoshimori.models


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0002_auto_20170625_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='transparent',
            field=models.ImageField(upload_to=hoshimori.models.uploadItem(b'c/transparent'), null=True, verbose_name='Transparent', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='irousvariation',
            name='is_large_irous',
            field=models.BooleanField(default=0, verbose_name='Large Irous'),
            preserve_default=False,
        ),
    ]
