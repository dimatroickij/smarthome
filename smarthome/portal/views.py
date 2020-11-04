from urllib.parse import urlparse

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from portal.forms import SmarthomeForm
from portal.models import AccessSmarthome, Smarthome


def home(request):
    if request.user.is_authenticated:
        countSmarthome = len(AccessSmarthome.objects.filter(user=request.user))
        if countSmarthome == 0 or countSmarthome > 1:
            return redirect('portal:settings')
        # elif countSmarthome == 1:
        #     return '1'
    return render(request, 'home.html')


@login_required
def settings(request):
    form = SmarthomeForm()
    mySmarthome = []
    for smarthome in AccessSmarthome.objects.filter(user=request.user, owner='owner'):
        pk = smarthome.smarthome.pk
        url = smarthome.smarthome.url
        token = smarthome.smarthome.token
        description = smarthome.smarthome.description
        owners = AccessSmarthome.objects.filter(smarthome=smarthome.smarthome)
        mySmarthome.append({'pk': pk, 'url': url, 'token': token,
                            'description': '' if description is None else description, 'owners': owners})
    return render(request, 'settings.html', {'form': form, 'mySmarthome': mySmarthome})


@login_required
def addSmarthome(request):
    if request.method == 'POST':
        form = SmarthomeForm(request.POST)
        if form.is_valid():
            site = urlparse(form.cleaned_data['url'])
            if site.scheme is None:
                messages.add_message(request, messages.ERROR, 'Введён неправильный URL')
            else:
                try:
                    headers = {'Authorization': "Bearer %s" % form.cleaned_data['token']}
                    query = requests.get(form.cleaned_data['url'] + '/api/', headers=headers, timeout=3)
                    if query.status_code not in ['200', '201']:
                        smarthome = form.save()
                        AccessSmarthome(smarthome=smarthome, user=request.user, owner='owner').save()
                        messages.add_message(request, messages.SUCCESS, 'Вы успешно добавили умный дом')
                        return redirect('portal:home')
                    elif query.status_code == '522':
                        messages.add_message(request, messages.ERROR, 'Сайт временно не доступен')
                except:
                    messages.add_message(request, messages.ERROR, 'Введённого URL не существует')
        return render(request, 'settings.html', {'form': form})


@login_required
def editDescription(request):
    try:
        smarthome = Smarthome.objects.get(pk=request.GET['pk'])
        if len(AccessSmarthome.objects.filter(smarthome=smarthome, user=request.user, owner='owner')) == 1:
            smarthome.description = request.GET['description']
            smarthome.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    except Smarthome.DoesNotExist:
        return HttpResponse(status=404)


def error_404(request, exception):
    return render(request, 'error/error404.html', status=404)
