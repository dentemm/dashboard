# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 21:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_request_last_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='last_update',
        ),
    ]