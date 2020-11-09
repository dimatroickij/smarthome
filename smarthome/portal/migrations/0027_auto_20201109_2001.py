# Generated by Django 3.1.3 on 2020-11-09 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0026_auto_20201109_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='codeDevice',
            field=models.CharField(blank=True, max_length=255, verbose_name='2 часть entity_id'),
        ),
        migrations.AlterField(
            model_name='device',
            name='domain',
            field=models.CharField(max_length=255, verbose_name='Domain (1 часть entity_id)'),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together={('domain', 'codeDevice')},
        ),
        migrations.RemoveField(
            model_name='device',
            name='entity_id',
        ),
    ]
