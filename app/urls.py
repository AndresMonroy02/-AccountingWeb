
from email.mime import audio
from re import template
from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    #urls de acceso


    #urls system
    path('login', views.login, name = 'login'),
    path('logout', views.logout_site, name = 'logout'),
    path('register', views.register, name = 'register'),

    #urls modulos
    path('expenses', views.expenses, name = 'expenses'),
    path('vehicules', views.vehicules, name = 'vehicules'),
    path('reports', views.reports, name = 'reports'),
    path('reportsViews/<str:report_id>/', views.show_reports, name = 'reportsViews'),

    #urls opciones
    path('edit', views.edit, name = 'edit'),
    path('edit/<str:expense_id>/', views.edit, name = 'edit'),

    #urls configuraciones 
    path('contact', views.contact, name = 'contact'),
    path("config", views.config, name = "config"),
    path('config/<str:user_id>/', views.config, name = 'config'),
    path('configedit/<str:user_id>/', views.configedit, name = 'configedit'),

    

]

