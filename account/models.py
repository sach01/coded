#from django.contrib.auth.models import AbstractUser, Group
#from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group 
#as AuthGroup


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    #user_group = models.ManyToManyField(CustomGroup, blank=True)

# class CustomUser(AbstractUser):
#     # email = models.EmailField(max_length=150, unique = True, blank=True)
#     # user_name = models.CharField(max_length=50, unique = True)
#     # first_name = models.CharField(max_length=50, blank=True)
#     # last_name = models.CharField(max_length=50, blank=True)
#     # phone_number = models.CharField(max_length=30, blank=True)
    
#     # date_joined = models.DateTimeField(auto_now_add=True)
#     # last_login = models.DateTimeField(auto_now_add=True)
#     # is_admin = models.BooleanField(default=False)
#     # is_staff = models.BooleanField(default=True)
#     # is_active = models.BooleanField(default=False)

#     ## Add custom fields if needed
#     name = models.CharField(max_length=50, blank=True)
#     mobile = models.CharField(max_length=10, blank=True)
#     is_active = models.BooleanField(default=True)
#     date_created = models.DateTimeField(null=True, blank=True)
#     user_group = models.ManyToManyField(CustomGroup, blank=True)


#     #bio = models.TextField(max_length=500, blank=True)
# class CustomGroup(models.Model):
#     name = models.CharField(max_length=150, unique=True)
#     members = models.ManyToManyField(CustomUser, blank=True)

#     def __str__(self):
#         return self.name
