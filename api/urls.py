from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('token', views.print_oauth_token),
    path('users', views.search_users),
    path('friends', views.friends)
]
