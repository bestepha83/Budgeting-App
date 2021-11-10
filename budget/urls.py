from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name = 'list'),
    path('add', views.ProjectCreateView.as_view(), name = 'add'),
    path('<slug:project_slug>', views.profile, name = 'profile'),
    path('<slug:project_slug>/transactions', views.transactions, name = 'transactions'),         
    path('expense_category_info', views.expense_category_info,
         name="expense_category_info"),
    path('<slug:project_slug>/analytics', views.analytics,
         name="analytics")
]