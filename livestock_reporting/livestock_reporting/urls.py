from django.urls import path, include
from livestock_reporting import views
from .views import Farmers_home, Farmers_case, MapView

urlpatterns = [  
    path('register/', views.register, name= "register"),
    path('login/', views.farmer_login, name= "login"),
    path('report/', views.report_case, name= "report_case"),
    path('logout/', views.farmer_logout, name='logout'),
    path('farm_home/', Farmers_home.as_view(), name='farm_home'),
    path('farm_home/case/<int:pk>', Farmers_case.as_view(), name='farm_case'),
    path('farm_home/map/<int:pk>', MapView.as_view(), name='map_view'),
    path('symptom_detail/<int:symptom_id>/', views.symptom_detail, name='symptom_detail')
]

