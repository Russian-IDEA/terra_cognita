from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('auth/', views.auth),
    path('logout/', views.logout_page),
    path('add/', views.add),
]