# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_auto_20170620_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='contact_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='person',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='identification_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='person',
            name='identification_type',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
