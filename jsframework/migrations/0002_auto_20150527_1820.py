# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jsframework', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
