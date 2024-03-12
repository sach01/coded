from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
#from .models import CustomUser
#from .forms import CustomUserForm
from functools import wraps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
#as AuthGroup

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import CustomUserForm, CustomGroupForm, CustomUserLoginForm

from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import CsrfViewMiddleware
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .decorators import group_required, allowed_users

@login_required
@group_required('Collector')
def create_group(request):
    if request.method == 'POST':
        form = CustomGroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            if not Group.objects.filter(name=group_name).exists():
                Group.objects.create(name=group_name)
                return redirect('group_list')
            else:
                error_message = "Group with this name already exists."
                return render(request, 'create_group.html', {'form': form, 'error_message': error_message})
    else:
        form = CustomGroupForm()
    return render(request, 'create_group.html', {'form': form})

@login_required(login_url="/account/login")
@allowed_users(allowed_roles=['Collector'])
@group_required('Collector')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

#def csrf_failure(request, reason=""):
#     # You can customize this function to handle CSRF failures as needed
 #   return render(request, 'error403.html', status=403)


def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ground')  # Assuming 'dashboard' is the name of your dashboard URL
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login3.html', {'form': form, 'error_message': error_message})
    else:
        form = CustomUserLoginForm()
    return render(request, 'login3.html', {'form': form})

# # def user_login(request):
# #     if request.method == 'POST':
# #         form = CustomUserLoginForm(request.POST)
# #         if form.is_valid():
# #             username = form.cleaned_data['username']
# #             password = form.cleaned_data['password']
# #             user = authenticate(request, username=username, password=password)
# #             if user is not None:
# #                 login(request, user)
# #                 # Redirect to a fixed URL after login (replace 'index' with your desired URL)
# #                 return redirect('index')
# #             else:
# #                 # Handle invalid credentials
# #                 error_message = "Invalid username or password."
# #         else:
# #             # Handle form validation errors
# #             error_message = "Form is not valid. Please check the input."
# #     else:
# #         form = CustomUserLoginForm()
# #         error_message = None

# #     return render(request, 'login.html', {'form': form, 'error_message': error_message})


# def user_login(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 # Redirect to a success page.
#                 return redirect('success_url')
#     else:
#         form = CustomUserForm()
#     return render(request, 'login2.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # Authenticate user
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirect to the next URL if it exists, otherwise redirect to a default URL
#             next_url = request.POST.get('next', 'user_list')
#             return redirect(next_url)
#                 # User is authenticated, log in the user
#                 ##login(request, user)
#                 # Redirect to a success page or homepage
#                 ##return redirect('user_list')
#         else:
#             # Authentication failed, display error message
#             messages.error(request, 'Invalid username or password.')

#     # Render the login page with a login form
#     return render(request, 'login2.html')

@login_required
@group_required('Collector')
def user_logout(request):
    logout(request)
    return redirect('login')


def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                content_type = ContentType.objects.get_for_model(CustomUser)
                permission_codename = f'view_{CustomUser._meta.model_name}'
                if request.user.has_perm(permission_codename, content_type):
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('unauthorized_page')
            else:
                return redirect('unauthorized_page')
        return wrapped_view
    return decorator

@login_required
@group_required('Collector')
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@group_required('Collector')
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

@login_required
@group_required('Collector')
def user_create(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.save()
            groups = form.cleaned_data.get('groups')  # Assuming you have a 'groups' field in your form
            if groups:
                user.groups.set(groups)  # Set the groups for the user
            return redirect('user_list')
    else:
        form = CustomUserForm()
    return render(request, 'user_form.html', {'form': form})

@login_required
@group_required('Collector')
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
@group_required('Collector')
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
@group_required('Collector')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

@login_required
@group_required('Collector')
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'group_detail.html', {'group': group})

@login_required
@group_required('Collector')
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
@group_required('Collector')
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = CustomGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = CustomGroupForm(instance=group)
    return render(request, 'group_form.html', {'form': form})

@login_required
@group_required('Collector')
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'group_confirm_delete.html', {'group': group})

@login_required
@group_required('Collector')
def list_and_add_permissions(request):
    groups = Group.objects.all()
    permissions = Permission.objects.all()
    
    if request.method == 'POST':
        group_id = request.POST.get('group')
        selected_permissions = request.POST.getlist('permissions')
        group = Group.objects.get(id=group_id)
        permissions_to_add = Permission.objects.filter(id__in=selected_permissions)
        group.permissions.add(*permissions_to_add)
        return redirect('group_list')  # Redirect to group listing page

    return render(request, 'list_and_add_permissions.html', {'groups': groups, 'permissions': permissions})

def unauthorized_page(request):
    return render(request, 'unauthorized_page.html')


# @login_required
# @group_required('Collector')
# def user_list(request):
#     users = CustomUser.objects.all()
#     return render(request, 'user_list.html', {'users': users})

# @login_required
# @group_required('admin')
# def user_detail(request, pk):
#     user = get_object_or_404(CustomUser, pk=pk)
#     return render(request, 'user_detail.html', {'user': user})

# @login_required
# @group_required('admin')
# def user_create(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = CustomUserForm()
#     return render(request, 'user_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def user_update(request, pk):
#     user = get_object_or_404(CustomUser, pk=pk)
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = CustomUserForm(instance=user)
#     return render(request, 'user_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def user_delete(request, pk):
#     user = get_object_or_404(CustomUser, pk=pk)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('user_list')
#     return render(request, 'user_confirm_delete.html', {'user': user})

# @login_required
# @group_required('admin')
# def group_list(request):
#     groups = Group.objects.all()
#     return render(request, 'group_list.html', {'groups': groups})

# @login_required
# @group_required('admin')
# def group_detail(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     return render(request, 'group_detail.html', {'group': group})

# @login_required
# @group_required('admin')
# def group_create(request):
#     if request.method == 'POST':
#         form = CustomGroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('group_list')
#     else:
#         form = CustomGroupForm()
#     return render(request, 'group_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def group_update(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     if request.method == 'POST':
#         form = CustomGroupForm(request.POST, instance=group)
#         if form.is_valid():
#             form.save()
#             return redirect('group_list')
#     else:
#         form = CustomGroupForm(instance=group)
#     return render(request, 'group_form.html', {'form': form})

# @login_required
# @group_required('admin')
# def group_delete(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     if request.method == 'POST':
#         group.delete()
#         return redirect('group_list')
#     return render(request, 'group_confirm_delete.html', {'group': group})

# @login_required
# def unauthorized_page(request):
#     return render(request, 'unauthorized_page.html')
