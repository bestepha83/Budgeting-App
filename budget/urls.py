from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view 

urlpatterns = [
    path('', views.accounts, name = 'list'),
    path('add', views.ProjectCreateView.as_view(), name = 'add'),
    path('<slug:project_slug>', views.profile, name = 'profile'),
    path('<slug:project_slug>/transactions', views.transactions, name = 'transactions'),
    path('register/', views.register, name ='register'),
    path('login/', auth_view.loginView.as_view(template_name='budget/login.html'), name = "login"),
    path('logout/', auth_view.logoutView.as_view(template_name='budget/logout.html'), name = "logout"),
]