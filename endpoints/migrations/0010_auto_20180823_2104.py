# Generated by Django 2.1 on 2018-08-23 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0009_auto_20180823_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='time',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
