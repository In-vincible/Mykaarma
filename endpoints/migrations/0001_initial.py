# Generated by Django 2.1 on 2018-08-15 12:52

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('vin', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Body')),
            ],
        ),
        migrations.CreateModel(
            name='Car_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('dealerId', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=80, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(geography=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Transmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='car_model',
            name='make',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Make'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Car_Model'),
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Color'),
        ),
        migrations.AddField(
            model_name='car',
            name='dealer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Dealer'),
        ),
        migrations.AddField(
            model_name='car',
            name='engine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Engine'),
        ),
        migrations.AddField(
            model_name='car',
            name='transmission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Transmission'),
        ),
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Year'),
        ),
    ]