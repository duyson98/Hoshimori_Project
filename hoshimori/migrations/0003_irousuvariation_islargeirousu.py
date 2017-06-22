# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0002_auto_20170622_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='irousuvariation',
            name='isLargeIrousu',
            field=models.BooleanField(default=1, verbose_name='Large Irousu'),
            preserve_default=False,
        ),
    ]
