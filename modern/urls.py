from django.urls import path
from django.contrib import admin
#from stalls.admin import custom_admin_site
#from django.contrib.admin.sites import catch_all_view
from modern import views as modern_views

from . import views
from django.urls import path
from . import views

urlpatterns = [
    path("", modern_views.index, name="index"),
    path("dashboard1", views.dashboard1, name="dashboard1"),

    path("ground", views.ground, name="ground"),
    path("dashboard1", views.dashboard1, name="dashboard1"),
    path("dashboard1", views.dashboard1, name="dashboard1"),

    path('get_user_permissions/', modern_views.get_user_permissions, name='get_user_permissions'),
    
    path('create_member/', modern_views.create_member, name='create_member'),
    path('create_inventory/', modern_views.create_inventory, name='create_inventory'),
    path('member_list/', modern_views.member_list, name='member_list'),
    path('inventory_list/', modern_views.inventory_list, name='inventory_list'),

    path("payment_plot", modern_views.payment_plot, name="payment_plot"),
    
    
    path("dashboard_bank", views.dashboard_bank, name="dashboard_bank"),
    path("bank_list", modern_views.bank_list, name="bank_list"),
    path("create_banker", modern_views.create_banker, name="create_banker"),

    path("register", modern_views.register, name="register"),
    path("edited_registers", modern_views.edited_registers, name="edited_registers"),
    path('edit_register/<int:register_id>/', modern_views.edit_register, name='edit_register'),
    path("list_registers", modern_views.list_registers, name="list_registers"),
    path("list_register_test", modern_views.list_register_test, name="list_register_test"),
    #path("list_registers2", modern_views.list_registers2, name="list_registers2"),
    #path("register_list3", modern_views.register_list3, name="register_list3"),
    path("get_rooms_by_floor", modern_views.get_rooms_by_floor, name="get_rooms_by_floor"),
    

    path("create_payment", modern_views.create_payment, name="create_payment"),
    path("autocomplete_register", modern_views.autocomplete_register, name="autocomplete_register"),
    #path('success_page', views.success_page, name='success_page'),
    
    path('owner_autocomplete/', modern_views.owner_autocomplete, name='owner_autocomplete'),

    path('get_owners/', modern_views.get_owners, name='get_owners'),
    #path('submit_payment/', modern_views.submit_payment, name='submit_payment'),
    #path('owner-autocomplete', modern_views.OwnerAutocomplete.as_view(), name='owner-autocomplete'),
    #path('room-autocomplete', modern_views.RoomAutocomplete.as_view(), name='room-autocomplete'),
    
    #path('get_owners/', modern_views.get_owners, name='get_owners'),
    
    path("register_balance", modern_views.register_balance, name="register_balance"),
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
    path('search_owners/', modern_views.search_owners, name='search_owners'),
    
    path('dashboard_rooms/', modern_views.dashboard_rooms, name='dashboard_rooms'),
    path('dashboard_register/', modern_views.dashboard_register, name='dashboard_register'),
    path('dashboard_payment/', modern_views.dashboard_payment, name='dashboard_payment'),
    path('dashboard_payment/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    #path('dashboard_payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('dashboard_payment/<int:payment_id>/edit/', views.edit_payment, name='edit_payment'),
    path('dashboard03/', modern_views.dashboard03, name='dashboard03'),
    path('dashboard04/', modern_views.dashboard04, name='dashboard04'),

    path('create_receiver/', modern_views.create_receiver, name='create_receiver'),
    path('list_receivers/', modern_views.list_receivers, name='list_receivers'),

    path('create_owner_type/', modern_views.create_owner_type, name='create_owner_type'),
    path('list_owner_type/', modern_views.list_owner_type, name='list_owner_type'),
    
    path('create_owner/', modern_views.create_owner, name='create_owner'),
    path('list_owner/', modern_views.list_owner, name='list_owner'),
    path('owner_detail/<int:pk>/', views.owner_detail, name='owner_detail'),
    path('owner_update/', modern_views.owner_update, name='owner_update'),
    path('owner_update/<int:pk>/', views.owner_update, name='owner_update'),
    path('owner_delete/<int:pk>/', views.owner_delete, name='owner_delete'),
    
    path('changelog/', modern_views.changelog, name='changelog'),

    path('list_register_test1/', modern_views.list_register_test1, name='list_register_test1'),

]

