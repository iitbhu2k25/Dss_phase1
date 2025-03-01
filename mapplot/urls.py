# mapplot/urls.py (app level)
from django.urls import path
from . import views

app_name = 'mapplot'

urlpatterns = [
    path('', views.shapefile_viewer, name='viewer'),
    path('get_shapefile_data/', views.get_shapefile_data, name='get_data'),
    path('upload_shapefile/', views.upload_shapefile, name='upload_shapefile'),
]