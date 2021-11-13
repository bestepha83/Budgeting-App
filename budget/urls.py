from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view 

urlpatterns = [
     path('', views.home, name='home'),
     path('register/', views.register, name='register'),
     path('login/', auth_view.LoginView.as_view(template_name='budget/login.html'), name="login"),
     path('logout/', auth_view.LogoutView.as_view(template_name='budget/logout.html'), name="logout"),
     path('accounts', views.accounts, name = 'list'),
     path('add', views.ProjectCreateView.as_view(), name = 'add'),
     path('<slug:project_slug>', views.profile, name = 'profile'),
     path('<slug:project_slug>/transactions', views.transactions, name = 'transactions'),         
     path('<slug:project_slug>/expense_category_info', views.expense_category_info,
          name="expense_category_info"),
     path('<slug:project_slug>/analytics', views.analytics,
          name="analytics"),
     path('<slug:project_slug>/stocks', views.stocks, name='stocks'),     
     path('<slug:project_slug>/stocks/<str:tid>', views.ticker, name='ticker'),
]