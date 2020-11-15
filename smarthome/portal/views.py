import json
import requests
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from portal.models import AccessSmarthome, Device, DeviceStates, Smarthome


def home(request):
    """
    :param request:
    :return:

    Главная страница портала. Показывается только неавторизованным пользователям. Если пользователь имеет доступ только
    к одному умному дому, то открывается страница :view:`portal.views.viewSmarthome`. Если у пользователя нет доступа ни к
    одному умному дому или есть доступ к нескольким, то открывается страница "Настройки" :view:`settings.views.settings`.

    **Context**

    ``countSmarthome`` Количество умных домов, доступных текущему пользователю.

    **Template**

    :template:`portal/home.html`
    """
    if request.user.is_authenticated:
        countSmarthome = len(AccessSmarthome.objects.filter(user=request.user, isConfirmed=True))
        if countSmarthome == 0 or countSmarthome > 1:
            return redirect('settings:settings')
        elif countSmarthome == 1:
            return redirect('portal:viewSmarthome', AccessSmarthome.objects.get(user=request.user, isConfirmed=True).pk)
    return render(request, 'home.html')


def getListId(x):
    try:
        device_class = x['attributes']['device_class']
    except:
        device_class = None
    try:
        icon = x['attributes']['icon']
    except:
        icon = None
    try:
        unit_of_measurement = x['attributes']['unit_of_measurement']
    except:
        unit_of_measurement = None

    return {'domain': x['entity_id'].split('.')[0], 'codeDevice': x['entity_id'].split('.')[1],
            'device_class': device_class, 'icon': icon, 'friendly_name': x['attributes']['friendly_name'],
            'unit_of_measurement': unit_of_measurement, 'state': {
            'state': x['state'], 'last_changed': x['last_changed'],
            'last_updated': x['last_updated']}}


def addState(x):
    x.state = DeviceStates.objects.filter(device_id=x.pk)[0]


@login_required
def viewSmarthome(request, pk):
    """
    :param request: Запрос от пользователя
    :param pk: Идентификатор записи из таблицы :model"`settings.AccessSmarthome`
    :return:

    Отображение данных умного дома на текущий момент. Если pk не найдено, то возвращается 404 ошибка.
    Если запись найдена, но принадлежит другому пользователю, то возвращается 403 ошибка.
    Если всё нормально, то возвращается страница с состоянием умного дома на данный момент.

    **Models**

    :model:`settings.AccessSmarthome`

    **Template**

    :template:`viewSmarthome.html`
    """
    access = AccessSmarthome.objects.filter(pk=pk, isConfirmed=True)
    if access.exists():
        if access[0].user == request.user:
            headers = {'Authorization': "Bearer %s" % access[0].smarthome.token}
            sensors = []
            lights = []
            switches = []
            groups = {'switch': 0, 'light': 0}
            state = {'off': 0, 'on': 1}
            try:
                responseDevice = requests.get(access[0].smarthome.url + '/api/states', headers=headers).json()
                devices = list(map(getListId, filter(lambda x: 'friendly_name' in list(x['attributes'].keys()),
                                                     responseDevice)))
                for device in devices:
                    pkDevice = ''
                    if Device.objects.filter(domain=device['domain'], codeDevice=device['codeDevice']).exists():
                        oldDevice = Device.objects.get(domain=device['domain'], codeDevice=device['codeDevice'])
                        oldDevice.friendly_name = device['friendly_name']
                        oldDevice.save()
                        pkDevice = oldDevice.pk
                    else:
                        newDevice = Device(smarthome=access[0].smarthome, domain=device['domain'].split('.')[0],
                                           codeDevice=device['codeDevice'], device_class=device['device_class'],
                                           friendly_name=device['friendly_name'], name=device['friendly_name'],
                                           icon=device['icon'], unit_of_measurement=device['unit_of_measurement'])
                        newDevice.save()
                        pkDevice = newDevice.pk
                    newDeviceStates = DeviceStates(device_id=pkDevice, state=device['state']['state'],
                                                   last_changed=device['state']['last_changed'],
                                                   last_updated=device['state']['last_updated'])
                    try:
                        newDeviceStates.full_clean()
                        newDeviceStates.save()
                    except ValidationError:
                        pass
            except:
                pass

            devices = Device.objects.filter(smarthome=access[0].smarthome).order_by('friendly_name')
            for device in devices:
                try:
                    stateRecord = DeviceStates.objects.filter(device=device)[0]
                    device.state = stateRecord.state
                    if device.domain in ['sensor', 'binary_sensor']:
                        sensors.append(device)
                    if device.domain == 'light':
                        lights.append(device)
                        groups[device.domain] += state[device.state]
                    if device.domain == 'switch':
                        switches.append(device)
                        groups[device.domain] += state[device.state]
                except IndexError:
                    pass

            if groups['switch'] != len(switches):
                groups['switch_state'] = 'toggle_off'
            else:
                groups['switch_state'] = 'toggle_on'

            if groups['light'] != len(lights):
                groups['light_state'] = 'toggle_off'
            else:
                groups['light_state'] = 'toggle_on'

            groups['light_len'] = len(lights)
            groups['switch_len'] = len(switches)
            return render(request, 'viewSmarthome.html', {'sensors': sensors, 'lights': lights, 'switches': switches,
                                                          'groups': groups, 'pk': access[0].pk})
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
@csrf_exempt
def selector(request):
    access = AccessSmarthome.objects.filter(pk=request.POST['pk'], isConfirmed=True)
    if access.exists():
        if access[0].user == request.user and access[0].access != 'guest':
            url = "%s/api/services/%s/%s" % (access[0].smarthome.url, request.POST['domain'], request.POST['service'])
            headers = {'Authorization': "Bearer %s" % access[0].smarthome.token}
            data = json.dumps({"entity_id": request.POST['entity_id']})
            try:
                response = requests.post(url, headers=headers, data=data)
            except:
                return HttpResponse(status=503)
            return HttpResponse(response.status_code)
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
def getStatesDevice(request):
    def transformState(x):
        if x.device.unit_of_measurement is not None:
            return x.state
        else:
            if x.state == 'off':
                return 0
            else:
                return 1
    access = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    if access.exists():
        if access[0].user == request.user and access[0].access != 'guest':
            devices = Device.objects.filter(domain=request.GET['entity_id'].split('.')[0],
                                            smarthome=access[0].smarthome,
                                            codeDevice=request.GET['entity_id'].split('.')[1])
            if devices.exists():
                states = DeviceStates.objects.filter(device=devices[0])
                if states.exists():
                    label = devices[0].unit_of_measurement
                    response = {'type': 'line', 'data': {
                        'labels': list(map(lambda x: x.last_changed.strftime('%d.%m %H:%M:%S'),
                                           states.order_by('last_changed'))),
                        'datasets': [{
                            #'backgroundColor': 'rgba(0, 0, 204, 0.9)',
                            'borderColor': 'rgba(0, 0, 204, 0.6)',
                            'label': label if label is not None else '0 - выключено, 1 - включено',
                            'data': list(map(transformState, states.order_by('last_changed'))),
                            'borderWidth': 1,
                            'steppedLine': True,
                            'fill': False
                        }]}, 'options': {'scales': {'yAxes': [{'ticks': {'beginAtZero': False}}]}}}
                    return JsonResponse(response, safe=False)
                return HttpResponse(status=204)
            return HttpResponse(status=400)
        return HttpResponse(status=403)
    return HttpResponse(status=404)


def error_404(request, exception):
    return render(request, 'error/error404.html', status=404)
