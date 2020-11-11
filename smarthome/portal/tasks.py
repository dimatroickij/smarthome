from datetime import datetime, timedelta

import requests
from celery import shared_task

# @shared_task
from django.core.exceptions import ValidationError
from django.utils import timezone

from portal.models import Smarthome, DeviceStates, Device


def iterateStates(device, pkDevice):
    def transformState(x):
        try:
            last_updated = x['last_updated']
        except KeyError:
            last_updated = x['last_changed']
        return {'last_changed': x['last_changed'], 'last_updated': last_updated, 'state': x['state']}

    for state in list(map(transformState, device[1:])):
        newDeviceStates = DeviceStates(device_id=pkDevice, state=state['state'],
                                       last_changed=state['last_changed'],
                                       last_updated=state['last_updated'])
        try:
            newDeviceStates.full_clean()
            newDeviceStates.save()
        except ValidationError:
            pass

@shared_task
def monitoringDeviceStates(seconds):
    startDate = (timezone.now() - timedelta(seconds=seconds)).strftime('%Y-%m-%dT%H:%M:%S%z')
    for smarthome in Smarthome.objects.all():
        headers = {'Authorization': "Bearer %s" % smarthome.token}
        params = {'minimal_response': ''}
        print(timezone.now())
        getStates = requests.get('%s/api/history/period/%s' % (smarthome.url, startDate), headers=headers,
                                 params=params)
        print(timezone.now())
        for device in getStates.json():
            domain = device[0]['entity_id'].split('.')[0]
            codeDevice = device[0]['entity_id'].split('.')[1]
            deviceRecord = Device.objects.filter(domain=domain, codeDevice=codeDevice, smarthome=smarthome)
            if deviceRecord.exists():
                iterateStates(device, deviceRecord[0].pk)
            else:
                try:
                    device_class = device[0]['attributes']['device_class']
                except:
                    device_class = ''
                try:
                    icon = device[0]['attributes']['icon']
                except:
                    icon = ''
                try:
                    unit_of_measurement = device[0]['attributes']['unit_of_measurement']
                except:
                    unit_of_measurement = ''
                # Для отсеивания лишних записей, которые скрыты в HomeAssistant, но приходят через этот запрос
                # (так как это поле обязательно, то запись не пройдёт валидацию)
                try:
                    friendly_name = device[0]['attributes']['friendly_name']
                except:
                    friendly_name = ''
                newDevice = Device(smarthome=smarthome, domain=domain, codeDevice=codeDevice, device_class=device_class,
                                   friendly_name=friendly_name, icon=icon, name=friendly_name,
                                   unit_of_measurement=unit_of_measurement)
                try:
                    newDevice.full_clean()
                    newDevice.save()
                    iterateStates(device, newDevice.pk)
                except ValidationError:
                    pass
        print(timezone.now())
