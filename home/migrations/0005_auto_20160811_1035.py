# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-11 08:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_processtoolresponsibles'),
    ]

    operations = [
        migrations.CreateModel(
            name='HWToolResponsibles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tool', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hw_responsibles', to='home.ToolPage')),
            ],
        ),
        migrations.RemoveField(
            model_name='toolresponsibles',
            name='responsible',
        ),
        migrations.RemoveField(
            model_name='toolresponsibles',
            name='tool',
        ),
        migrations.DeleteModel(
            name='ToolResponsibles',
        ),
    ]
