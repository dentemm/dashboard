# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-14 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20160614_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolpage',
            name='tool_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
