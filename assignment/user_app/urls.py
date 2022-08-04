from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createUser),
    path('login/', views.login),
    path('logout/', views.logout),
    path('valid/', views.userValid),
]