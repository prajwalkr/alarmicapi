# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('phNum', models.IntegerField(serialize=False, primary_key=True)),
                ('gcmId', models.CharField(max_length=100)),
            ],
        ),
    ]
