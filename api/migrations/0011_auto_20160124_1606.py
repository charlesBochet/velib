# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-24 15:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20160122_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 24, 15, 6, 50, 277516, tzinfo=utc)),
        ),
    ]
