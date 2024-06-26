from django.urls import path, include
from . import views 

urlpatterns = [
    path('population_list', views.population_list, name='population_list'),
    path('population_filter', views.population_filter, name='population_filter'),
    path('population_list_pdf', views.population_list_pdf, name='population_list_pdf'),
    ]