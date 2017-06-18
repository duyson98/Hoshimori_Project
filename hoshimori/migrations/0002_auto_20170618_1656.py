# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='unlock',
            field=models.CharField(max_length=100, verbose_name='Unlock at'),
            preserve_default=True,
        ),
    ]
