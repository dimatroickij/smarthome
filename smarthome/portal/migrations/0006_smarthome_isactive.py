# Generated by Django 3.1.2 on 2020-11-02 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20201102_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='smarthome',
            name='isActive',
            field=models.BooleanField(default=True, verbose_name='Доступность умного дома (нужно для мониторинга)'),
        ),
    ]
