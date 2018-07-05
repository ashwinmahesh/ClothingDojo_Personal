# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-29 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clothing_admin', '0014_auto_20180628_2304'),
        ('clothing_dojo', '0019_auto_20180628_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='batch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='clothing_admin.Batch'),
        ),
    ]