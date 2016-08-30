# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 17:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20160829_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('description', models.TextField()),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.DashboardUser')),
            ],
        ),
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rejection_reason', models.CharField(max_length=256)),
                ('status', models.IntegerField(choices=[(0, 'Requested'), (1, 'Accepted'), (2, 'Rejected'), (3, 'Planned')], default=0)),
                ('last_update', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
