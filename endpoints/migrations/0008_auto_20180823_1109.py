# Generated by Django 2.1 on 2018-08-23 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0007_auto_20180822_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Car_Model'),
        ),
    ]