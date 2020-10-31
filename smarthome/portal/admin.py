from django.contrib import admin

# Register your models here.
from portal.models import Device, Smarthome, AccessSmarthome

admin.site.register(Smarthome)
admin.site.register(AccessSmarthome)
admin.site.register(Device)