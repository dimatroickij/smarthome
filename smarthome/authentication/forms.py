from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})

        # self.username_field = 'username'
        self.fields['username'].label = 'Логин'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Введите email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widget=forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = widget=forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = widget = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2',)