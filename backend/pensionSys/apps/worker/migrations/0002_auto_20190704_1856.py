# Generated by Django 2.2.1 on 2019-07-04 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='birthday',
            field=models.CharField(max_length=50),
        ),
    ]
