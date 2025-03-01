from django.urls import path
from .views import get_raster,visual_home,get_raster_lists

urlpatterns = [
    path('',visual_home,name="raster_visual"),
    path('categories/',get_raster,name="raster_categories"),
    path('raster_data/<str:category>/',get_raster_lists,name="raster_details"),
]
