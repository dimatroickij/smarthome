import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Smarthome(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField('URL', max_length=255, unique=True)
    token = models.CharField('Token умного дома', max_length=255)
    description = models.CharField('Описание умного дома', max_length=255, blank=True)

    def __str__(self):
        return self.url + ' - ' + self.token

    class Meta:
        ordering = ['url']
        verbose_name = 'Умный дом'
        verbose_name_plural = 'умные дома'


class AccessSmarthome(models.Model):
    OWNER = (('guest', 'Гость'),
             ('owner', 'Владелец'))
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smarthome = models.ForeignKey(Smarthome, on_delete=models.CASCADE, verbose_name='ID умного дома')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    owner = models.CharField('', max_length=5, choices=OWNER, null=True)

    def __str__(self):
        return self.smarthome.description + ' - ' + self.user.username

    class Meta:
        ordering = ['user']
        verbose_name = 'уровень доступа к умному дому'
        verbose_name_plural = 'Уровень доступа к умному дому'
        unique_together = [['smarthome', 'user']]


class Device(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smarthome = models.ForeignKey(Smarthome, on_delete=models.CASCADE, verbose_name='ID умного дома')
    user_id = models.CharField('user_id', max_length=255, unique=True, blank=True)
    device_class = models.CharField('Класс устройства', max_length=255)
    friendly_name = models.CharField('friendly_name', max_length=255, blank=False)
    icon = models.CharField('Иконка', max_length=255, blank=True)
    unit_of_measurement = models.CharField('unit_of_measurement', max_length=255, blank=True)
    entity_id = models.CharField('entity_id', max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.smarthome.url + ' - ' + self.user_id

    class Meta:
        ordering = ['user_id']
        verbose_name = 'устройство'
        verbose_name_plural = 'Устройства'
