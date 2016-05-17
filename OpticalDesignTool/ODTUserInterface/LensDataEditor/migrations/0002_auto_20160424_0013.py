# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-24 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LensDataEditor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surface',
            name='surfaceConicConstant',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='surface',
            name='surfaceDecenterX',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='surface',
            name='surfaceDecenterY',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='surface',
            name='surfaceRadius',
            field=models.FloatField(default=25.0),
        ),
        migrations.AddField(
            model_name='surface',
            name='surfaceThickness',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='surface',
            name='surfaceVertexCurvature',
            field=models.FloatField(default=0.0),
        ),
    ]
