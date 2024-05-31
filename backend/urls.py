from django.urls import path, include
from backend import views

urlpatterns = [
    path('', views.landing), 
    path('home/', views.index),
    path('home/<str:name>', views.district), 

]