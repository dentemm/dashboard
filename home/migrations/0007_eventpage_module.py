# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-19 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20160819_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='home.ToolModule'),
        ),
    ]
