"""smarthome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from authentication.forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path('settings/', include('settings.urls')),
    path('', include('authentication.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html',
                                                         authentication_form=LoginForm,
                                                         redirect_authenticated_user='/')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        form_class=MyPasswordResetForm, html_email_template_name='registration/password_reset_email.html')),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=MySetPasswordForm)),
    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',
                                               form_class=MyPasswordChangeForm)),
    path('accounts/', include('django.contrib.auth.urls')),
]

handler404 = 'portal.views.error_404'
