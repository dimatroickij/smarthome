# Generated by Django 3.1.3 on 2020-11-08 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_remove_smarthome_isdelete'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Device',
        ),
    ]