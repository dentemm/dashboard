# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_safeworkingpermit_safeworkingpermituser_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='SafeworkingPermitTool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tools', to='home.SafeWorkingPermit')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ToolPage')),
            ],
        ),
    ]