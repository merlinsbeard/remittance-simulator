# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_remittance_date_paid_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remittance',
            name='date_paid_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
