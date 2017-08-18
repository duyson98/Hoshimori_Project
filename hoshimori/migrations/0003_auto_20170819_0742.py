# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0002_auto_20170724_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='level',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='easy_stage',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='hard_stage',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='materials',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='normal_stage',
        ),
        migrations.AddField(
            model_name='account',
            name='story_progress',
            field=models.PositiveIntegerField(help_text='Which episode have you cleared?', null=True, verbose_name='Story Progress', db_index=True, validators=[django.core.validators.MaxValueValidator(112)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownedcard',
            name='_cache_atk',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='ATK'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownedcard',
            name='_cache_def',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='DEF'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownedcard',
            name='_cache_hp',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='HP'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownedcard',
            name='_cache_sp',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='SP'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownedcard',
            name='level',
            field=models.PositiveIntegerField(default=50, null=True, verbose_name='Level'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stage',
            name='chapter',
            field=models.CharField(max_length=50, null=True, verbose_name='Chapter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stagedifficulty',
            name='drops',
            field=models.CharField(max_length=200, null=True, verbose_name='Drops'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stagedifficulty',
            name='stage',
            field=models.ForeignKey(related_name='stage_with_difficulty', on_delete=django.db.models.deletion.SET_NULL, to='hoshimori.Stage', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='game_id',
            field=models.CharField(help_text='You can find it in-game. It is a series of 8 characters.', max_length=8, verbose_name='Game ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill_affinity',
            field=models.PositiveIntegerField(default=1, null=True, verbose_name='Skill Affinity', choices=[(0, b'None'), (1, b'Ignore weapon affinity'), (2, b'Ignore conflicting weapon affinity')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stagedifficulty',
            name='objectives',
            field=models.CharField(max_length=400, null=True, verbose_name='Objectives'),
            preserve_default=True,
        ),
    ]
