from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.home, name='home'),
    path('smarthome/add', views.addSmarthome, name='addSmarthome'),
    path('smarthome/editDescription', views.editDescription, name='editDescription'),
    path('settings', views.settings, name='settings'),
]
