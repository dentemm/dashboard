# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_dashboarduser_dummy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboarduser',
            name='dummy',
        ),
        migrations.RemoveField(
            model_name='task',
            name='completed',
        ),
        migrations.AddField(
            model_name='task',
            name='single',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(0, 'To Do'), (1, 'In Progress'), (2, 'Done'), (3, 'Proposed'), (4, 'rejected')], default=0),
        ),
    ]