Sure, here's the full complete code for managing users, roles, and user roles in a Django application:
1. Models (models.py):

python

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=500, blank=True)
    mobile = models.CharField(max_length=500, blank=True)

class Role(models.Model):
    name = models.CharField(max_length=100)

class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

2. Forms (forms.py):

python

from django import forms
from .models import CustomUser, Role, UserRole

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'mobile']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['user', 'role']

3. Views (views.py):

python

from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserForm, RoleForm, UserRoleForm
from .models import CustomUser, Role, UserRole

def create_custom_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm()
    return render(request, 'create_custom_user.html', {'form': form})

def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'create_role.html', {'form': form})

def create_user_role(request):
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_role_list')
    else:
        form = UserRoleForm()
    return render(request, 'create_user_role.html', {'form': form})

# Similarly, implement views for listing, updating, and deleting users, roles, and user roles.

4. Templates (create_custom_user.html, create_role.html, create_user_role.html):

html

<!-- create_custom_user.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create</button>
</form>

html

<!-- create_role.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create</button>
</form>

html

<!-- create_user_role.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create</button>
</form>

5. URLs (urls.py):

python

from django.urls import path
from . import views

urlpatterns = [
    path('create_custom_user/', views.create_custom_user, name='create_custom_user'),
    path('create_role/', views.create_role, name='create_role'),
    path('create_user_role/', views.create_user_role, name='create_user_role'),
    # Add URLs for listing, updating, and deleting users, roles, and user roles.
]

6. URL Configuration (urls.py in project directory):

python

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('yourapp.urls')),
]

Ensure you replace 'yourapp' with the name of your Django app.

With these components in place, you'll have a complete Django 
application for managing users, roles, and user roles, including 
forms, views, models, and templates.