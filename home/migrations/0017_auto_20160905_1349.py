# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_request_importance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='rejection_reason',
            field=models.TextField(null=True),
        ),
    ]
