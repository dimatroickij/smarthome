# Generated by Django 3.1.2 on 2020-11-02 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20201101_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smarthome',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание умного дома'),
        ),
    ]
