# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='i_rarity',
            field=models.PositiveIntegerField(verbose_name='Rarity', choices=[(0, '\u2605'), (1, '\u2605\u2605'), (2, '\u2605\u2605\u2605'), (3, '\u2605\u2605\u2605\u2605'), (4, '\u2605\u2605\u2605\u2605\u2605')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weaponupgrade',
            name='i_rarity',
            field=models.PositiveIntegerField(default=0, verbose_name='Rarity', choices=[(0, '\u2605'), (1, '\u2605\u2605'), (2, '\u2605\u2605\u2605'), (3, '\u2605\u2605\u2605\u2605'), (4, '\u2605\u2605\u2605\u2605\u2605')]),
            preserve_default=True,
        ),
    ]
