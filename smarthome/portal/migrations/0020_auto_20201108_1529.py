# Generated by Django 3.1.3 on 2020-11-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_auto_20201108_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(default=models.CharField(max_length=255, verbose_name='Название из HomeAssistant'), max_length=255, verbose_name='Введённоё название устройства'),
        ),
    ]