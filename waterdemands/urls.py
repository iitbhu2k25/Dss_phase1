from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_demand_page, name='demand_page'),
    path("waterdemand/get_locations/", views.get_locations, name="get_locations"),
    path('waterdemand/get_floating/', views.get_floating, name='get_floating'),
    path('waterdemand/get_combined_population/', views.get_combined_population, name='get_combined_population'),
]
