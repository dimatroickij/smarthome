# Generated by Django 3.1.2 on 2020-11-05 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_smarthome_isactive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesssmarthome',
            name='owner',
        ),
        migrations.AddField(
            model_name='accesssmarthome',
            name='access',
            field=models.CharField(choices=[('guest', 'Гость'), ('owner', 'Владелец')], max_length=5, null=True, verbose_name=''),
        ),
    ]
