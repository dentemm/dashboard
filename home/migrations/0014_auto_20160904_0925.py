# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-04 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20160903_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
