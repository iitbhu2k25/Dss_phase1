from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='sewage_home'),
    path("waterdemand/get_locations/", views.get_locations, name="get_locations"),
    path('waterdemand/get_floating/', views.get_floating, name='get_floating'),
    path('waterdemand/get_combined_population/', views.get_combined_population, name='get_combined_population'),

]
