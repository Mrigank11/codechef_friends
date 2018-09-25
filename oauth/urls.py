from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('redirect', views.oauth_redirect),
    path('callback', views.oauth_callback),
]
