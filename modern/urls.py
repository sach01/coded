from django.urls import path
from django.contrib import admin
#from stalls.admin import custom_admin_site
#from django.contrib.admin.sites import catch_all_view
from modern import views as modern_views

from . import views

urlpatterns = [
    path("", modern_views.index, name="index"),
    #path("dashboard", views.dashboard, name="dashboard"),
    #path("display_details", views.display_details, name="display_details"),
    #path("display_payment_details", views.display_payment_details, name="display_payment_details"),
    #path("payment_details", views.payment_details, name="payment_details"),
    ##path('payment_details/<int:owner_id>/', views.payment_details, name='payment_details'),

    path("register", modern_views.register, name="register"),
    path("edited_registers", modern_views.edited_registers, name="edited_registers"),
    path('edit_register/<int:register_id>/', modern_views.edit_register, name='edit_register'),
    path("list_registers", modern_views.list_registers, name="list_registers"),
    path("list_register_test", modern_views.list_register_test, name="list_register_test"),
    path("list_registers2", modern_views.list_registers2, name="list_registers2"),
    path("register_list3", modern_views.register_list3, name="register_list3"),
    path("get_rooms_by_floor", modern_views.get_rooms_by_floor, name="get_rooms_by_floor"),
    

    path("create_payment", modern_views.create_payment, name="create_payment"),
    #path('success_page', views.success_page, name='success_page'),
    path("payment_list", modern_views.payment_list, name="payment_list"),
    #path("display_payment_details", views.display_payment_details, name="display_payment_details"),
    #path("payment_details", views.payment_details, name="payment_details"),
    #path("list_details", views.list_details, name="list_details"),

    
    path("list_registers_part1", modern_views.list_registers_part1, name="list_registers_part1"),
    path("duplicate_payment_rows", modern_views.duplicate_payment_rows, name="duplicate_payment_rows"),
    path('get_rooms_and_floor', modern_views.get_rooms_and_floor, name='get_rooms_and_floor'),
    path('get_owner_name', modern_views.get_owner_name, name='get_owner_name'),
    path('get_owner_data/', modern_views.get_owner_data, name='get_owner_data'),
    path('get_room_and_owner/', modern_views.get_room_and_owner, name='get_room_and_owner'),

    
    path('create_payment_test/', modern_views.create_payment_test, name='create_payment_test'),
    path('create_payment_test/<int:register_id>/', modern_views.create_payment_test, name='create_payment_test'),
    path('create_payment_test2/', modern_views.create_payment_test2, name='create_payment_test2'),
    path('create_payment_test2/<int:register_id>/', modern_views.create_payment_test2, name='create_payment_test2'),
    
    path('dashboard_rooms/', modern_views.dashboard_rooms, name='dashboard_rooms'),
    path('dashboard_register/', modern_views.dashboard_register, name='dashboard_register'),
    path('dashboard_payment/', modern_views.dashboard_payment, name='dashboard_payment'),
    path('dashboard_payment/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    #path('dashboard_payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('dashboard_payment/<int:payment_id>/edit/', views.edit_payment, name='edit_payment'),

    path('create_receiver/', modern_views.create_receiver, name='create_receiver'),
    

    
    path('list_register_test1/', modern_views.list_register_test1, name='list_register_test1'),


]

