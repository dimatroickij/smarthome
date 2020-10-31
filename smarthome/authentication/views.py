from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from authentication.tokens import account_activation_token
from authentication.forms import MyUserCreationForm, MyModelForm


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Подтвердите email для завершения регистрации')
                return redirect('portal:home')
        else:
            form = MyUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return redirect('portal:home')


@login_required
def editProfile(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Вы успешно изменили учётные данные')
            return redirect('portal:home')
    else:
        form = MyModelForm(instance=request.user)
    return render(request, 'registration/editProfile.html', {'form': form})


def passwordDone(request):
    messages.add_message(request, messages.SUCCESS, 'Ваш пароль успешно изменён')
    return redirect('portal:home')


def resetDone(request):
    messages.add_message(request, messages.SUCCESS, 'Ваш пароль был сохранен. Теперь вы можете войти.')
    return redirect('portal:home')


def activate(request, uidb64, token):
    try:
        uid = int(urlsafe_base64_decode(uidb64))
        print(uid)
        user = get_user_model().objects.get(pk=uid)
        print(user.username)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Email подтверждён. Выполнен вход на сайт.')
    else:
        messages.add_message(request, messages.SUCCESS, 'Ошибка подтверждения email')
    return redirect('portal:home')
