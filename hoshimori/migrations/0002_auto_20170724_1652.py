# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='i_weapon',
            field=models.PositiveIntegerField(verbose_name='Weapon', choices=[(0, 'Sword'), (1, 'Spear'), (2, 'Hammer'), (3, 'Gun'), (4, 'Rod'), (5, 'Gunblade'), (6, 'Twin Barrett'), (7, 'Claw Fang')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='irous',
            name='guard',
            field=multiselectfield.db.fields.MultiSelectField(default=b'', max_length=100, null=True, verbose_name='Guard', choices=[(0, 'Sword'), (1, 'Spear'), (2, 'Hammer'), (3, 'Gun'), (4, 'Rod'), (5, 'Gunblade'), (6, 'Twin Barrett'), (7, 'Claw Fang')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='irous',
            name='strong',
            field=multiselectfield.db.fields.MultiSelectField(default=b'', max_length=100, null=True, verbose_name='Strong', choices=[(0, 'Sword'), (1, 'Spear'), (2, 'Hammer'), (3, 'Gun'), (4, 'Rod'), (5, 'Gunblade'), (6, 'Twin Barrett'), (7, 'Claw Fang')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='irous',
            name='weak',
            field=multiselectfield.db.fields.MultiSelectField(default=b'', max_length=100, null=True, verbose_name='Weak', choices=[(0, 'Sword'), (1, 'Spear'), (2, 'Hammer'), (3, 'Gun'), (4, 'Rod'), (5, 'Gunblade'), (6, 'Twin Barrett'), (7, 'Claw Fang')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stagedifficulty',
            name='difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Difficulty', choices=[(0, b'Easy'), (1, b'Normal'), (2, b'Hard'), (3, b'EX')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weapon',
            name='i_type',
            field=models.PositiveIntegerField(verbose_name='Weapon', choices=[(0, 'Sword'), (1, 'Spear'), (2, 'Hammer'), (3, 'Gun'), (4, 'Rod'), (5, 'Gunblade'), (6, 'Twin Barrett'), (7, 'Claw Fang')]),
            preserve_default=True,
        ),
    ]
