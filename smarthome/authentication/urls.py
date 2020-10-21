from django.urls import path

from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('accounts/registration/', views.registration, name='registration'),
    path('accounts/password_change/done/', views.passwordDone, name='passwordDone'),
    path('accounts/reset/done/', views.resetDone, name='resetDone'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
]
