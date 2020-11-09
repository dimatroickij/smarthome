# Generated by Django 3.1.3 on 2020-11-08 15:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0017_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceStates',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=255, verbose_name='Состояние устройства')),
                ('last_changed', models.DateTimeField(verbose_name='Последнее изменение состояния')),
                ('last_updated', models.DateTimeField(verbose_name='Последнее обновление')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.device', verbose_name='Устройство')),
            ],
        ),
    ]