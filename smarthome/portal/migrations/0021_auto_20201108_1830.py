# Generated by Django 3.1.3 on 2020-11-08 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0020_auto_20201108_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'verbose_name': 'устройство', 'verbose_name_plural': 'Устройства'},
        ),
        migrations.RemoveField(
            model_name='device',
            name='idDevice',
        ),
    ]
