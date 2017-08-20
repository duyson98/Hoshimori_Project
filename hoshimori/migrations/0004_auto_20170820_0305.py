# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import hoshimori.models


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0003_auto_20170819_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='_cache_total_senseis',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='mini_body',
            field=models.ImageField(default=0, upload_to=hoshimori.models.uploadItem(b's'), verbose_name='Chibi'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='mini_icon',
            field=models.ImageField(default=0, upload_to=hoshimori.models.uploadItem(b's'), verbose_name='Chibi Icon'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='story_progress',
            field=models.PositiveIntegerField(help_text='Which episode have you cleared?', null=True, verbose_name='Story Progress', db_index=True, validators=[django.core.validators.MaxValueValidator(116)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stagedifficulty',
            name='stage',
            field=models.ForeignKey(related_name='stage_with_difficulty', to='hoshimori.Stage', null=True),
            preserve_default=True,
        ),
    ]
