# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-15 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubcarapp', '0006_auto_20160914_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='location',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
