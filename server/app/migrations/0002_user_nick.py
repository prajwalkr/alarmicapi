# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nick',
            field=models.CharField(default=datetime.datetime(2015, 10, 2, 16, 37, 37, 232000, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
