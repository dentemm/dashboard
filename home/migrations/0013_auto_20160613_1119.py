# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_task_tool'),
    ]

    operations = [
        migrations.AddField(
            model_name='safeworkingpermit',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='safeworkingpermit',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='due_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
