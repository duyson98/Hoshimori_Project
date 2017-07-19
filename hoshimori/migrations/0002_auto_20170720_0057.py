# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ownedcard',
            name='evolved',
        ),
        migrations.RemoveField(
            model_name='ownedcard',
            name='level',
        ),
        migrations.RemoveField(
            model_name='ownedcard',
            name='obtained_date',
        ),
        migrations.AlterField(
            model_name='student',
            name='description',
            field=models.CharField(max_length=100, null=True, verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='japanese_name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Name (Japanese)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='unlock',
            field=models.CharField(max_length=100, null=True, verbose_name='Unlock at'),
            preserve_default=True,
        ),
    ]
