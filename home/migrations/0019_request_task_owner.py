# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_request_planned_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='task_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.DashboardUser'),
        ),
    ]