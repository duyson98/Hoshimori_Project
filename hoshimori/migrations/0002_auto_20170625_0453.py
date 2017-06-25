# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hoshimori.models


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='introduction_1',
            field=models.FileField(default='', upload_to=hoshimori.models.uploadItem(b's/voices'), verbose_name='Introduction 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='introduction_2',
            field=models.FileField(default='', upload_to=hoshimori.models.uploadItem(b's/voices'), verbose_name='Introduction 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='phrase_1',
            field=models.FileField(default='', upload_to=hoshimori.models.uploadItem(b's/voices'), verbose_name='Phrase 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='phrase_2',
            field=models.FileField(default='', upload_to=hoshimori.models.uploadItem(b's/voices'), verbose_name='Phrase 2'),
            preserve_default=False,
        ),
    ]
