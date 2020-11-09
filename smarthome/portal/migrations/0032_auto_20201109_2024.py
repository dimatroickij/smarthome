# Generated by Django 3.1.3 on 2020-11-09 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0031_auto_20201109_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='codeDevice',
            field=models.CharField(max_length=255, verbose_name='2 часть entity_id'),
        ),
        migrations.AlterField(
            model_name='device',
            name='domain',
            field=models.CharField(max_length=255, verbose_name='Domain (1 часть entity_id)'),
        ),
    ]
