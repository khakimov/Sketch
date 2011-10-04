from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':75}), label=_('Username'))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_('Password'))
    

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':75}), label=_('Username'))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_('Password'))
    email    = forms.EmailField()
    
    def clean_username(self):
        try:
           User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
             return self.cleaned_data['username']
        raise forms.ValidationError("This username is already in use. Please choose another.")
    
    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            password=self.cleaned_data['password'],
                                            email = self.cleaned_data['email'])
        return new_user