# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_module_toolpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleToolJoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.Module')),
                ('tool', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='home.ToolPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]