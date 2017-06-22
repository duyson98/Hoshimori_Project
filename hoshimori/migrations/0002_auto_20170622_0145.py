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
        migrations.CreateModel(
            name='FavoriteCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card', models.ForeignKey(related_name='fans', to='hoshimori.Card')),
                ('owner', models.ForeignKey(related_name='favoritecards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OwnedCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evolved', models.BooleanField(default=False, verbose_name='Evolved')),
                ('level', models.PositiveIntegerField(verbose_name='Level')),
                ('obtained_date', models.DateField(null=True, verbose_name='Obtained Date', blank=True)),
                ('account', models.ForeignKey(related_name='ownedcards', to='hoshimori.Account')),
                ('card', models.ForeignKey(related_name='owned', to='hoshimori.Card')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='favoritecard',
            unique_together=set([('owner', 'card')]),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.PositiveIntegerField(default=0, verbose_name='Card Type', choices=[(0, 'Normal'), (1, 'Extra'), (2, 'Subcard')]),
            preserve_default=True,
        ),
    ]
