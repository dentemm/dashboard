# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20160904_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='importance',
            field=models.IntegerField(choices=[(0, 'Nice To Have'), (1, 'Important'), (2, 'Critical')], default=0),
        ),
    ]
