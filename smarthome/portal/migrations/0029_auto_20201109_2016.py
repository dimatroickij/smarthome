# Generated by Django 3.1.3 on 2020-11-09 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0028_auto_20201109_2015'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set(),
        ),
    ]