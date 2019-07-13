# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-06 03:39
from __future__ import unicode_literals

import apps.camera.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0005_interaction_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='area_log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(max_length=100)),
                ('upper_wear_fg', models.CharField(max_length=100)),
                ('cellphone', models.CharField(max_length=100)),
                ('orientation', models.CharField(max_length=100)),
                ('headwear', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=100)),
                ('glasses', models.CharField(max_length=100)),
                ('bag', models.CharField(max_length=100)),
                ('upper_wear_texture', models.CharField(max_length=100)),
                ('lower_wear', models.CharField(max_length=100)),
                ('upper_color', models.CharField(max_length=100)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=apps.camera.models.area_log.get_path)),
            ],
        ),
    ]