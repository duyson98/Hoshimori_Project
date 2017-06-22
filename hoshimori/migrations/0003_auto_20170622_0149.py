# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0002_auto_20170622_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nakayoshi',
            name='effect_level',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Effect Level', choices=[(0, b'Small'), (1, b'Medium'), (2, b'Large'), (3, b'Super')]),
            preserve_default=True,
        ),
    ]
