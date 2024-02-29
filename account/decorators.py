# accounts/decorators.py
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

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

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                # Redirect to unauthorized page or perform any other action
                return redirect('unauthorized_page')
        return wrapped_view
    return decorator


#######################################
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def group_required(group_names):
    """
    Decorator for views that checks whether a user is in a certain group.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper
    return decorator

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
