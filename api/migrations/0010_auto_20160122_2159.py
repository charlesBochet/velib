# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-22 20:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20160122_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 20, 59, 36, 301162, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='stationlog',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]