# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0004_auto_20170622_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='ID', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='level',
            field=models.PositiveIntegerField(default=70, verbose_name='Level', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(70)]),
            preserve_default=True,
        ),
    ]
