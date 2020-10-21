from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def error_404(request, exception):
    return render(request, 'error/error404.html', status=404)
