from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('auth/', views.auth),
    path('logout/', views.logout_page),
    path('post/', views.post),
    path('satellits/', views.get_satellites_json),
    path('download/<int:order_id>/', views.download),
]