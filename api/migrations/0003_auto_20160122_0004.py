# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-21 23:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160102_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 21, 23, 4, 25, 171070, tzinfo=utc)),
        ),
    ]
