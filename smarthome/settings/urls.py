from django.urls import path

from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings, name='settings'),
    path('addSmarthome', views.addSmarthome, name='addSmarthome'),
    path('deleteSmarthome', views.deleteSmarthome, name='deleteSmarthome'),
    path('checkAccess', views.checkAccess, name='checkAccess'),
    path('editDescription', views.editDescription, name='editDescription'),
    path('addUserSmarthome', views.addUserSmarthome, name='addUserSmarthome'),
    path('editAccessSmarthome', views.editAccessSmarthome, name='editAccessSmarthome'),
    path('deleteAccessSmarthome', views.deleteAccessSmarthome, name='deleteAccessSmarthome'),
    path('approveInvitation/<int:response>', views.approveInvitation, name='approveInvitation')
]
