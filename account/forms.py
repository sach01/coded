from django import forms
#from .models import CustomUser
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.models import Group

class CustomGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']  # Add or remove fields as needed

class CustomUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'groups')
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# class CustomUserForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'email')  # Add any additional fields here

# You can directly use Django's AuthenticationForm for login

class AuthorizationForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all())




"""
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'mobile']


class CustomGroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ['name', 'members']
"""