# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-11 11:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20160811_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboarduser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='dashboarduser',
            name='last_name',
        ),
    ]
