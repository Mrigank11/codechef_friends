from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('token', views.print_access_token),
    path('users', views.search_users),
    path('friends', views.friends),
    path('friends/<str:username>', views.get_friend_info)
]
