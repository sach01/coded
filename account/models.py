#from django.contrib.auth.models import AbstractUser, Group
#from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group 
#as AuthGroup

#from django.contrib.auth.models import AbstractUser
import requests

def get_external_ip():
    try:
        # Use a service like ipify.org to fetch the external IP
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json().get('ip')
        else:
            # If fetching fails, return None or handle the error accordingly
            return None
    except Exception as e:
        # Handle exceptions
        print("Error fetching external IP:", e)
        return None

class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    #user_group = models.ManyToManyField(CustomGroup, blank=True)

    # # def save(self, *args, **kwargs):
    # #     request = kwargs.pop('request', None)

    # #     if not self.pk:
    # #         action = 'CREATE'
    # #     else:
    # #         action = 'UPDATE'

    # #     ip_address = get_external_ip()  # Fetch external IP address
    # #     if ip_address:
    # #         self.ip_address = ip_address  # Set the IP address in the model

    # #     super().save(*args, **kwargs)

    # #     if request:
    # #         if self.pk:  # If user is already created (not on creation)
    # #             if self.last_login:  # If user has logged in
    # #                 action = 'LOGIN'
    # #             else:
    # #                 action = 'LOGOUT'
    # #             ChangeLog.objects.create(
    # #                 user=self,
    # #                 action=action,
    # #                 ip_address=ip_address or 'Unknown'
    # #             )


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
