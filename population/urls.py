from django.urls import path
from . import views

app_name = "population"
urlpatterns =[
  path("",views.prediction_methods_page,name="prediction_methods_page"),
  path('time-series/',views.time_series_based_page,name="time_series_based_page"),
  path('scenario-based/',views.scenario_based_page,name="scenario_based_page"),
  path('cohort-based/',views.cohort_component_based_page,name="cohort_component_based_page"),
  path('demographic-based/',views.demographic_based_page,name="demographic_based_page"),
  path('get-states/', views.get_states, name='get_states'),
  path('get-districts/<int:state_code>/', views.get_districts, name='get_districts'),
  path('get-subdistricts/<int:state_code>/<int:district_code>/', views.get_subdistricts, name='get_subdistricts'),
  path('get-villages/<int:state_code>/<int:district_code>/<int:subdistrict_code>/', views.get_villages, name='get_villages'),
  path('calculate/', views.calculate_projection, name='calculate_projection'),
  path('calculate-demographic/', views.calculate_demographic_projection, name = 'calculate_demographic_projection'),
  
  # path('get-regions/', views.get_regions, name='get_regions'),
  # path('get-demographic-data/', views.get_demographic_data, name = "get_demographic_data"),
]