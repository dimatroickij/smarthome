from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from authentication.forms import MyUserCreationForm


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Подтвердите email для завершения регистрации')
                return redirect('main:home')
        else:
            form = MyUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return render(request, 'registration/signup.html', )