from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.home, name='home'),
    path('smarthome/<str:pk>', views.viewSmarthome, name='viewSmarthome')
]
