# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-05 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0004_fall_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='interaction_log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]