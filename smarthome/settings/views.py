from urllib.parse import urlparse

import requests
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from portal.forms import SmarthomeForm
from portal.models import AccessSmarthome, Smarthome


@login_required
def settings(request):
    form = SmarthomeForm()
    mySmarthome = []
    invitationsToSmarthome = AccessSmarthome.objects.filter(user=request.user, isConfirmed=False)
    for smarthome in AccessSmarthome.objects.filter(user=request.user, isConfirmed=True):
        url = smarthome.smarthome.url
        token = 'Доступен для владельца умного дома' if smarthome.access == 'guest' else smarthome.smarthome.token
        description = smarthome.smarthome.description
        usersWithAccess = AccessSmarthome.objects.filter(smarthome=smarthome.smarthome)
        mySmarthome.append({'pk': smarthome.pk, 'url': url, 'token': token, 'access': smarthome.access,
                            'description': '' if description is None else description,
                            'usersWithAccess': usersWithAccess})
    return render(request, 'settings.html', {'form': form, 'mySmarthome': mySmarthome,
                                             'countMySmarthome': len(mySmarthome),
                                             'invitationsToSmarthome': invitationsToSmarthome,
                                             'countInvitations': len(invitationsToSmarthome)})


@login_required
def addSmarthome(request):
    if request.method == 'POST':
        form = SmarthomeForm(request.POST)
        if form.is_valid():
            site = urlparse(form.cleaned_data['url'])
            if site.scheme is None:
                form.add_error('url', ValidationError('Введён неправильный URL'))
            else:
                try:
                    headers = {'Authorization': "Bearer %s" % form.cleaned_data['token']}
                    query = requests.get(form.cleaned_data['url'] + '/api/', headers=headers, timeout=3)
                    if query.status_code not in ['200', '201']:
                        smarthome = form.save()
                        AccessSmarthome(smarthome=smarthome, user=request.user, access='owner', isConfirmed=True).save()
                        messages.add_message(request, messages.SUCCESS, 'Вы успешно добавили умный дом')
                        return redirect('portal:home')
                    elif query.status_code == '522':
                        form.add_error('url', ValidationError('Сайт временно не доступен'))
                except:
                    form.add_error('url', ValidationError('Введённого URL не существует'))
        countMySmarthome = len(AccessSmarthome.objects.filter(user=request.user, isConfirmed=True))
        invitationsToSmarthome = len(AccessSmarthome.objects.filter(user=request.user, isConfirmed=False))
        return render(request, 'settings.html', {'form': form, 'countMySmarthome': countMySmarthome,
                                                 'countInvitations': invitationsToSmarthome})


@login_required
def deleteSmarthome(request):
    access = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    if access.exists():
        if AccessSmarthome.objects.filter(smarthome=access[0].smarthome, user=request.user, access='owner',
                                          isConfirmed=True).exists():
            pass
            # editAccess = access[0]
            # editAccess.access = request.GET['access']
            # editAccess.save()
            return redirect('settings:settings')
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
def checkAccess(request):
    smarthome = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    if smarthome.exists():
        if smarthome[0].user == request.user and smarthome[0].access == 'owner':
            return HttpResponse(status=200)
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
def editDescription(request):
    access = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    if access.exists():
        if access[0].user == request.user and access[0].access == 'owner':
            smarthome = Smarthome.objects.get(pk=access[0].smarthome.pk)
            smarthome.description = request.GET['description']
            smarthome.save()
            return HttpResponse(status=200)
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
def addUserSmarthome(request):
    access = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    if access.exists():
        if access[0].user == request.user and access[0].access == 'owner':
            user = get_user_model().objects.filter(username=request.GET['user'])
            if user.exists():
                newAccessUserSmarthome = AccessSmarthome(user=user[0], smarthome=access[0].smarthome,
                                                         access=request.GET['owner'])
                try:
                    newAccessUserSmarthome.full_clean()
                    newAccessUserSmarthome.save()
                    text = """<div class="col mb-4">
                                <div class="card h-100">
                                    <div class="card-body">
                                        <button type="button" class="close" data-dismiss="alert" aria-label="Close"
                                        onclick="deleteAccess(this, '%s')">
                                            <span aria-hidden="true">×</span>
                                        </button>
                                        <h5 class="card-title">%s</h5>
                                        <p class="card-text">%s</p>
                                        <a href="#" class="card-link" onclick="editAccess(this, '%s')">Изменить
                                                уровень доступа</a>
                                    </div>
                                    <div class="updateTrack">
                                        Приглашение отправлено
                                    </div>
                                </div>
                            </div>""" % (newAccessUserSmarthome.pk, newAccessUserSmarthome.user.username,
                                         newAccessUserSmarthome.get_access_display(), newAccessUserSmarthome.pk)
                    return HttpResponse(text)
                except ValidationError:
                    return HttpResponse(208)
            return HttpResponse(400)
        return HttpResponse(403)
    return HttpResponse(404)


@login_required
def editAccessSmarthome(request):
    access = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    if access.exists():
        if AccessSmarthome.objects.filter(smarthome=access[0].smarthome, user=request.user, access='owner',
                                          isConfirmed=True).exists() and access[0].user != request.user:
            editAccess = access[0]
            editAccess.access = request.GET['access']
            editAccess.save()
            return redirect('settings:settings')
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
def deleteAccessSmarthome(request):
    access = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    if access.exists():
        if AccessSmarthome.objects.filter(smarthome=access[0].smarthome, user=request.user, access='owner',
                                          isConfirmed=True).exists() and access[0].user != request.user:
            deleteAccess = access[0]
            deleteAccess.delete()
            return HttpResponse(status=200)
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
def deleteSmarthome(request):
    smarthome = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=True)
    pkSmarthome = smarthome[0].smarthome.pk
    if smarthome.exists():
        if smarthome[0].user == request.user and smarthome[0].access == 'owner':
            Smarthome.objects.get(pk=pkSmarthome).delete()
            return HttpResponse(status=200)
        return HttpResponse(status=403)
    return HttpResponse(status=404)


@login_required
def approveInvitation(request, response):
    invitation = AccessSmarthome.objects.filter(pk=request.GET['pk'], isConfirmed=False)
    if invitation.exists():
        if invitation[0].user == request.user:
            if response:
                saveInvitation = invitation[0]
                saveInvitation.isConfirmed = True
                saveInvitation.save()
            else:
                invitation[0].delete()
            return redirect('settings:settings')
        return HttpResponse(status=403)
    return HttpResponse(status=404)
