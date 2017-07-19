# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hoshimori.models


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0002_auto_20170720_0057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.AlterUniqueTogether(
            name='favoritecard',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='favoritecard',
            name='card',
        ),
        migrations.RemoveField(
            model_name='favoritecard',
            name='owner',
        ),
        migrations.DeleteModel(
            name='FavoriteCard',
        ),
        migrations.RemoveField(
            model_name='weapon',
            name='image',
        ),
        migrations.AddField(
            model_name='ownedcard',
            name='evolved',
            field=models.BooleanField(default=False, verbose_name='Evolved'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='weaponupgrade',
            name='image',
            field=models.ImageField(default=False, upload_to=hoshimori.models.uploadItem(b'w'), verbose_name='Icon'),
            preserve_default=False,
        ),
    ]
