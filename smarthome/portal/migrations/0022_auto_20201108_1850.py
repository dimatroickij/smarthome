# Generated by Django 3.1.3 on 2020-11-08 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0021_auto_20201108_1830'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='devicestates',
            unique_together={('device', 'state', 'last_changed', 'last_updated')},
        ),
    ]
