# Generated by Django 3.1.3 on 2020-11-08 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0018_devicestates'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devicestates',
            options={'ordering': ['device', 'last_updated'], 'verbose_name': 'состояние устройства', 'verbose_name_plural': 'Состояния устройств'},
        ),
    ]