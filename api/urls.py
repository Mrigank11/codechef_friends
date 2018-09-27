from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('token', views.print_access_token),
    path('users', views.search_users),
    path('following', views.following),
    path('followers', views.followers),
    path('following/<str:username>', views.get_friend_info),
]
