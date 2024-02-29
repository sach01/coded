Here's the full complete code, including the custom group_required decorator, 
views, models, forms, and templates:
1. Models (models.py):

python

from django.contrib.auth.models import AbstractUser, Group as AuthGroup
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=500, blank=True)
    mobile = models.CharField(max_length=500, blank=True)

class CustomGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
    members = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name

2. Forms (forms.py):

python

from django import forms
from .models import CustomUser, CustomGroup

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'mobile']

class CustomGroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ['name', 'members']

3. Views (views.py):

python

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from .models import CustomUser, CustomGroup
from .forms import CustomUserForm, CustomGroupForm
from functools import wraps
from django.shortcuts import redirect

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect('unauthorized_page')
        return wrapped_view
    return decorator

@login_required
@group_required('admin')
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@group_required('admin')
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

@login_required
@group_required('admin')
def user_create(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm()
    return render(request, 'user_form.html', {'form': form})

@login_required
@group_required('admin')
def user_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

@login_required
@group_required('admin')
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
@group_required('admin')
def group_list(request):
    groups = CustomGroup.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

@login_required
@group_required('admin')
def group_detail(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    return render(request, 'group_detail.html', {'group': group})

@login_required
@group_required('admin')
def group_create(request):
    if request.method == 'POST':
        form = CustomGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = CustomGroupForm()
    return render(request, 'group_form.html', {'form': form})

@login_required
@group_required('admin')
def group_update(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    if request.method == 'POST':
        form = CustomGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = CustomGroupForm(instance=group)
    return render(request, 'group_form.html', {'form': form})

@login_required
@group_required('admin')
def group_delete(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'group_confirm_delete.html', {'group': group})

@login_required
def unauthorized_page(request):
    return render(request, 'unauthorized_page.html')

4. Templates:

    user_list.html
    user_detail.html
    user_form.html
    user_confirm_delete.html
    group_list.html
    group_detail.html
    group_form.html
    group_confirm_delete.html
    unauthorized_page.html

You need to create these templates in your templates directory.
5. URLs (urls.py):

python

from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/update/', views.group_update, name='group_update'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),

    path('unauthorized/', views.unauthorized_page, name='unauthorized_page'),
]

6. URL Configuration (urls.py in project directory):

python

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('yourapp.urls')),
]

Replace 'yourapp' with the name of your Django app.

With these components in place, you'll have a Django application with 
views protected by the group_required 
decorator, ensuring that only users belonging to specific groups can access them.

Below are templates for each of the pages you mentioned:
user_list.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User List</title>
</head>
<body>
    <h1>User List</h1>
    <ul>
    {% for user in users %}
        <li><a href="{% url 'user_detail' user.pk %}">{{ user.username }}</a></li>
    {% endfor %}
    </ul>
    <a href="{% url 'user_create' %}">Create User</a>
</body>
</html>

user_detail.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Detail</title>
</head>
<body>
    <h1>User Detail</h1>
    <p>Username: {{ user.username }}</p>
    <p>First Name: {{ user.first_name }}</p>
    <p>Last Name: {{ user.last_name }}</p>
    <p>Email: {{ user.email }}</p>
    <p>Age: {{ user.age }}</p>
    <a href="{% url 'user_update' user.pk %}">Update</a>
    <a href="{% url 'user_delete' user.pk %}">Delete</a>
</body>
</html>

user_form.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Form</title>
</head>
<body>
    <h1>User Form</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
</body>
</html>

user_confirm_delete.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Confirm Delete</title>
</head>
<body>
    <h1>Confirm Delete</h1>
    <p>Are you sure you want to delete user "{{ user.username }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, delete</button>
    </form>
</body>
</html>

group_list.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Group List</title>
</head>
<body>
    <h1>Group List</h1>
    <ul>
    {% for group in groups %}
        <li><a href="{% url 'group_detail' group.pk %}">{{ group.name }}</a></li>
    {% endfor %}
    </ul>
    <a href="{% url 'group_create' %}">Create Group</a>
</body>
</html>

group_detail.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Group Detail</title>
</head>
<body>
    <h1>Group Detail</h1>
    <p>Name: {{ group.name }}</p>
    <a href="{% url 'group_update' group.pk %}">Update</a>
    <a href="{% url 'group_delete' group.pk %}">Delete</a>
</body>
</html>

group_form.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Group Form</title>
</head>
<body>
    <h1>Group Form</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
</body>
</html>

group_confirm_delete.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Confirm Delete</title>
</head>
<body>
    <h1>Confirm Delete</h1>
    <p>Are you sure you want to delete group "{{ group.name }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, delete</button>
    </form>
</body>
</html>

unauthorized_page.html

html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Unauthorized Access</title>
</head>
<body>
    <h1>Unauthorized Access</h1>
    <p>You do not have permission to access this page.</p>
</body>
</html>

Ensure you place these templates in 
the appropriate directory within your 
Django project's templates folder. Adjust the 
HTML as needed to fit your project's styling and requirements.


'''
class CustomUser(AbstractUser):
    # Add custom fields if needed
    name = models.CharField(max_length=500, blank=True)
    mobile = models.CharField(max_length=500, blank=True)
'''
'''
    #bio = models.TextField(max_length=500, blank=True)
class CustomGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
    members = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name
'''