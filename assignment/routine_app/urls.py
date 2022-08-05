from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createRoutine.as_view()),
]