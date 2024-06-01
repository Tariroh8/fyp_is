from django.urls import path, include
from vetapp import views
from .views import vet_home

urlpatterns = [
    path('vet_home/', views.vet_home, name='vet_home'), #vets homepage
    path('vet_register/', views.vet_register, name= "vet_register"),
    path('vet_login/', views.vet_login, name= "vet_login"),
    path('ward/<str:district_foreign>/<str:ward_name>/', views.ward_map_view, name='ward_map'),
    path('download_cases_csv/', views.download_cases_csv, name='download_cases_csv'),
    path('national_stats/', views.national_vet_statistics, name='national_stats'),
    path('cases_map/', views.cases_map, name='cases_map'),
    path('symptom_create/', views.symptom_create, name='symptom_create'),
    path('symptoms/', views.symptom_list, name='symptom_list'),

]