from django.urls import path
from . import views
#from account import views as account_views

urlpatterns = [
    #path("", views.index, name="index"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('user_list/', views.user_list, name='user_list'),
    path('user_detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('user_create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    path('group_list/', views.group_list, name='group_list'),
    path('group_detail/<int:pk>/', views.group_detail, name='group_detail'),
    path('group_create/', views.group_create, name='group_create'),
    path('group_update/<int:pk>/update/', views.group_update, name='group_update'),
    path('group_delete/<int:pk>/delete/', views.group_delete, name='group_delete'),

    path('unauthorized/', views.unauthorized_page, name='unauthorized_page'),

    path('list_and_add_permissions/', views.list_and_add_permissions, name='list_and_add_permissions'),


    #################################################################
    path('create-group/', views.create_group, name='create_group'),
    path('group-list/', views.group_list, name='group_list'),
]
