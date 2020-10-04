import uuid

from django.db import models


# Create your models here.
class Device(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField('user_id', max_length=255, unique=True, blank=True)
    device_class = models.CharField('Класс устройства', max_length=255)
    friendly_name = models.CharField('friendly_name', max_length=255, blank=False)
    icon = models.CharField('Иконка', max_length=255, blank=True)
    unit_of_measurement = models.CharField('unit_of_measurement', max_length=255, blank=True)
    entity_id = models.CharField('entity_id', max_length=255, unique=True, blank=True)
