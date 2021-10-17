from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name = 'list'),
    path('add', views.ProjectCreateView.as_view(), name = 'add'),
    path('<slug:project_slug>', views.profile, name = 'detail')
]