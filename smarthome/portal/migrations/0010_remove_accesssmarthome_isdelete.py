# Generated by Django 3.1.2 on 2020-11-05 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_auto_20201105_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesssmarthome',
            name='isDelete',
        ),
    ]