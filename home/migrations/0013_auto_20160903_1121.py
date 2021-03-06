# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-03 11:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('home', '0012_auto_20160902_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilitystatuspage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='toolutilitystatusvalue',
            name='status',
        ),
        migrations.RemoveField(
            model_name='toolutilitystatusvalue',
            name='tool',
        ),
        migrations.RemoveField(
            model_name='utility',
            name='fab',
        ),
        migrations.RemoveField(
            model_name='utility',
            name='status',
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['event', 'owner']},
        ),
        migrations.DeleteModel(
            name='Fab',
        ),
        migrations.DeleteModel(
            name='FacilityStatusPage',
        ),
        migrations.DeleteModel(
            name='ToolUtilityStatusValue',
        ),
        migrations.DeleteModel(
            name='Utility',
        ),
        migrations.DeleteModel(
            name='UtilityStatus',
        ),
    ]
