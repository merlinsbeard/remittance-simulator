# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 10:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0003_auto_20170620_0630'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance',
            name='date_paid_out',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 6, 21, 10, 40, 7, 227897, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
