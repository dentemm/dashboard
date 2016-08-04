# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 11:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_safeworkingpermittool'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='safeworkingpermit',
            name='vwv_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.DashboardUser'),
        ),
        migrations.AlterField(
            model_name='safeworkingpermituser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.DashboardUser'),
        ),
    ]