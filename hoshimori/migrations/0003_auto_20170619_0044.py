# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0002_auto_20170618_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weaponeffect',
            name='i_name',
            field=models.PositiveIntegerField(null=True, verbose_name='Weapon Effect', choices=[(0, b'GAY')]),
            preserve_default=True,
        ),
    ]
