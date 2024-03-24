# accounts/decorators.py
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from functools import wraps
from .models import CustomUser

def group_required(group_name):
    """
    Decorator for views that checks whether a user belongs to a specific group.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            user_has_permission = CustomUser.objects.filter(groups__name=group_name, id=request.user.id).exists()
            if request.user.is_authenticated and user_has_permission:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('unauthorized_page')
        return wrapped_view
    return decorator

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapped_func(request, *args, **kwargs):
            #print("working: ", allowed_roles)
            group=None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        return wrapped_func
    return decorator

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
    return wrapper_func


# def group_required(group_name):
#     """
#     Decorator for views that checks whether a user belongs to a specific group.
#     """
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapped_view(request, *args, **kwargs):
#             if request.user.is_authenticated:
#                 user_has_permission = Group.objects.filter(name=group_name, user=request.user).exists()
#                 if user_has_permission:
#                     return view_func(request, *args, **kwargs)
#                 else:
#                     return redirect('unauthorized_page')
#             else:
#                 return redirect('unauthorized_page')
#         return wrapped_view
#     return decorator


# def group_required(group_name):
#     """
#     Decorator for views that checks whether a user belongs to a specific group.
#     """
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#             if request.user.groups.filter(name=group_name).exists():
#                 return view_func(request, *args, **kwargs)
#             else:
#                 raise PermissionDenied("You do not have permission to access this resource.")
#                 #return None
#         return wrapper
#     return decorator

# def group_required(group_name):
#     """
#     Decorator for views that checks whether a user belongs to a specific group.
#     """
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             if request.user.groups.filter(name=group_name).exists():
#                 return view_func(request, *args, **kwargs)
#             else:
#                 raise PermissionDenied("You do not have permission to access this resource.")
#         return wrapper
#     return decorator

##########################################################

# def group_required(group_name):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if request.user.groups.filter(name=group_name).exists():
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponseForbidden("You don't have permission to access this page.")
#         return _wrapped_view
#     return decorator

# def group_required(group_name):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapped_view(request, *args, **kwargs):
#             if request.user.groups.filter(name=group_name).exists():
#                 return view_func(request, *args, **kwargs)
#             else:
#                 # Redirect to unauthorized page or perform any other action
#                 return redirect('unauthorized_page')
#         return wrapped_view
#     return decorator

###########################################

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
# from django.http import HttpResponseForbidden

# def group_required(group_names):
#     """
#     Decorator for views that checks whether a user is in a certain group.
#     """
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#             if request.user.groups.filter(name__in=group_names).exists():
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponseForbidden("You do not have permission to access this page.")
#         return wrapper
#     return decorator

def login_and_group_required(group_names):
    """
    Decorator for views that checks whether a user is logged in and in a certain group.
    """
    def decorator(view_func):
        login_decorator = login_required(view_func)
        group_decorator = group_required(group_names)(login_decorator)
        return group_decorator
    return decorator

# @login_and_group_required(['admin', 'staff'])
# def my_view(request):
#     # View code here
