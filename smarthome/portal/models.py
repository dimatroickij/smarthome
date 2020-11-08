import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Smarthome(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField('URL', max_length=255, unique=True)
    token = models.CharField('Token умного дома', max_length=255)
    description = models.CharField('Описание умного дома', max_length=255, blank=True, default='')
    isActive = models.BooleanField('Доступность умного дома (нужно для мониторинга)', default=True)

    def __str__(self):
        return self.url

    class Meta:
        ordering = ['url']
        verbose_name = 'Умный дом'
        verbose_name_plural = 'умные дома'


class AccessSmarthome(models.Model):
    ACCESS = (('guest', 'Гость'),
              ('owner', 'Владелец'))
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smarthome = models.ForeignKey(Smarthome, on_delete=models.CASCADE, verbose_name='ID умного дома')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    access = models.CharField('', max_length=5, choices=ACCESS, null=True)
    isConfirmed = models.BooleanField('Пользователь подтвердил запрос', default=False)

    def __str__(self):
        return self.smarthome.url + ' - ' + self.user.username

    class Meta:
        ordering = ['user']
        verbose_name = 'уровень доступа к умному дому'
        verbose_name_plural = 'Уровень доступа к умному дому'
        unique_together = [['smarthome', 'user']]


class Device(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smarthome = models.ForeignKey(Smarthome, on_delete=models.CASCADE, verbose_name='ID умного дома')
    entity_id = models.CharField('ID для изменения состояния устройства', max_length=255, unique=True)
    device_class = models.CharField('Класс устройства', max_length=255, blank=False, null=True)
    friendly_name = models.CharField('Название из HomeAssistant', max_length=255)
    name = models.CharField('Введённоё название устройства', max_length=255)
    icon = models.CharField('Иконка для сенсоров', max_length=255, blank=True, null=True)
    unit_of_measurement = models.CharField('Единица измерения', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.smarthome.url + ' - ' + self.entity_id

    class Meta:
        verbose_name = 'устройство'
        verbose_name_plural = 'Устройства'


class DeviceStates(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    state = models.CharField('Состояние устройства', max_length=255)
    last_changed = models.DateTimeField('Последнее изменение состояния')
    last_updated = models.DateTimeField('Последнее обновление')

    def __str__(self):
        return self.device.friendly_name + ' - ' + self.state

    class Meta:
        ordering = ['-last_updated']
        verbose_name = 'состояние устройства'
        verbose_name_plural = 'Состояния устройств'
        unique_together = [['device', 'state', 'last_changed', 'last_updated']]