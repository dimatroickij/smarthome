import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from portal.models import AccessSmarthome


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
            devices = [{}]
            sensors = []
            lights = []
            switches = []
            groups = {'switch': 0, 'light': 0}
            state = {'off': 0, 'on': 1}
            try:
                devices = requests.get(access[0].smarthome.url + '/api/states', headers=headers).json()
            except:
                pass  # TODO Добавить получение старых данных, если дом недоступен
            for device in devices:
                # TODO Добавить обработку полученных устройств для сохранения или обновления их данных в БД портала
                if device['entity_id'].split('.')[0] == 'sensor':
                    sensors.append(device)
                if device['entity_id'].split('.')[0] == 'light':
                    lights.append(device)
                    groups[device['entity_id'].split('.')[0]] += state[device['state']]
                if device['entity_id'].split('.')[0] == 'switch':
                    switches.append(device)
                    groups[device['entity_id'].split('.')[0]] += state[device['state']]
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
                                                          'groups': groups})
        return HttpResponse(status=403)
    return HttpResponse(status=404)


def error_404(request, exception):
    return render(request, 'error/error404.html', status=404)
