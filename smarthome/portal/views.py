from django.http import HttpResponse
from django.shortcuts import render, redirect
from portal.models import AccessSmarthome


def home(request):
    if request.user.is_authenticated:
        countSmarthome = len(AccessSmarthome.objects.filter(user=request.user, isConfirmed=True))
        if countSmarthome == 0 or countSmarthome > 1:
            return redirect('settings:settings')
        # elif countSmarthome == 1:
        #     return '1'
    return render(request, 'home.html')

def viewSmarthome(request, pk):
    return HttpResponse(status=200)

def error_404(request, exception):
    return render(request, 'error/error404.html', status=404)
