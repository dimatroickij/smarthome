from django.contrib import admin
from portal.models import Device, Smarthome, AccessSmarthome, DeviceStates


@admin.register(Smarthome)
class SmarthomeAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'url', 'description', 'isActive')


@admin.register(AccessSmarthome)
class AccessSmarthome(admin.ModelAdmin):
    list_display = ('unique_id', 'smarthome', 'user', 'access', 'isConfirmed')
    list_filter = ['smarthome']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('smarthome', 'domain', 'codeDevice', 'name', 'friendly_name', 'device_class', 'icon',
                    'unit_of_measurement')
    list_filter = ['smarthome']


@admin.register(DeviceStates)
class DeviceStatesAdmin(admin.ModelAdmin):
    list_display = ('device', 'state', 'last_changed', 'last_updated')
