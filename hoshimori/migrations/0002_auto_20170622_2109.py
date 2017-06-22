# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hoshimori', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='owner',
            field=models.ForeignKey(related_name='added_stages', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stage',
            name='part',
            field=models.CharField(max_length=50, null=True, verbose_name='Part'),
            preserve_default=True,
        ),
    ]
