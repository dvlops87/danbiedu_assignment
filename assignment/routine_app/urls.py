from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createRoutine.as_view()),
    path('get/list/', views.CheckListRoutine.as_view()),
    path('get/', views.CheckRoutine.as_view()),
]