# Generated by Django 2.1 on 2018-08-23 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('endpoints', '0008_auto_20180823_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searches',
            name='car',
        ),
        migrations.AddField(
            model_name='searches',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='searches',
            name='object_id',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='searches',
            name='time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
