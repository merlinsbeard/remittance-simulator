# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 02:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('country', models.CharField(default='Philippines', max_length=255)),
                ('identification_type', models.CharField(max_length=255)),
                ('identification_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Remittance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_reference_number', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('payout_amount', models.IntegerField()),
                ('payout_currency', models.CharField(default='PH', max_length=10)),
                ('slug', models.SlugField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('PAID', 'PAID'), ('CANCELLED', 'CANCELLED')], default='AVAILABLE', max_length=100)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiary', to='partner.Person')),
                ('remitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remitter', to='partner.Person')),
            ],
        ),
    ]