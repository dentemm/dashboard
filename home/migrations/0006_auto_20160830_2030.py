# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 20:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_request_requeststatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['owner']},
        ),
        migrations.AddField(
            model_name='request',
            name='requisition_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.RequestStatus'),
        ),
    ]
