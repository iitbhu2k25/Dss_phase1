from django.contrib import admin
from django.urls import path
from .views import stp_home,GetStatesView,GetDistrictView,GetSubDistrictView,GetVillageView,GetTableView,GetRankView,GetBoundry,GetVillage_UP
urlpatterns = [
    path('', stp_home, name='index'),
    path('get_states/',GetStatesView, name='get_states'),
    path('get_districts/',GetDistrictView, name='get_districts_data'),
    path('get_sub_districts/',GetSubDistrictView, name='get_sub_districts'),
    path('get_villages/',GetVillageView, name='get_villages'),
    path('table/',GetTableView, name='get_table'),
    path('get_rankings/',GetRankView, name='get_rank'),
    path('get_boundary/',GetBoundry, name='get_default_boundary'),
    path('get_village_boundary/',GetVillage_UP,name='village_boundry')

    
]
