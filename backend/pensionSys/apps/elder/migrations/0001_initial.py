# Generated by Django 2.2.1 on 2019-07-03 09:17

import apps.elder.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='elder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=11)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(max_length=5)),
                ('id_card', models.CharField(max_length=30)),
                ('fam_name', models.CharField(max_length=30)),
                ('fam_phone', models.CharField(max_length=11)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=apps.elder.models.elder.get_photo_path)),
            ],
        ),
    ]
