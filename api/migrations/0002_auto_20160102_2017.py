# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 19:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 19, 17, 24, 473175, tzinfo=utc)),
        ),
    ]
