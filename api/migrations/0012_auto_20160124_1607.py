# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-24 15:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20160124_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 24, 15, 7, 0, 909124, tzinfo=utc)),
        ),
    ]
