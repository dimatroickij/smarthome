from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.home, name='home'),
    path('selector', views.selector, name='selector'),
    path('smarthome/<str:pk>', views.viewSmarthome, name='viewSmarthome'),
    path('getStatesDevice', views.getStatesDevice, name='getStatesDevice'),
    path('editNameDevice', views.editNameDevice, name='editNameDevice')
]
