from django import forms

from portal.models import Smarthome


class SmarthomeForm(forms.ModelForm):
    # url = forms.CharField(label='Введите URL', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # token = forms.CharField(label='Введите токен', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # description = forms.CharField(label='Введите описание', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Smarthome
        fields = ('url', 'token', 'description',)
        widgets = {'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://domain'}),
                   'token': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'})}
