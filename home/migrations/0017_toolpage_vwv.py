# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-14 05:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20160614_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolpage',
            name='vwv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toolen', to='home.SafeWorkingPermit'),
        ),
    ]
