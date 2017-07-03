# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 05:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.IntegerField()),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('COMPLETE', 'COMPLETE'), ('PAID', 'PAID'), ('CANCELLED', 'CANCELLED')], default='AVAILABLE', max_length=100)),
                ('is_deposit', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
