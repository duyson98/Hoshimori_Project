# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoshimori', '0003_irousuvariation_islargeirousu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irousuvariation',
            name='isLargeIrousu',
            field=models.NullBooleanField(verbose_name='Large Irousu'),
            preserve_default=True,
        ),
    ]
