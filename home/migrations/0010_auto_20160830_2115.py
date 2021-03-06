# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_remove_request_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='request',
            name='rejection_reason',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.IntegerField(choices=[(0, 'Requested'), (1, 'Accepted'), (2, 'Rejected'), (3, 'Planned')], default=0),
        ),
    ]
