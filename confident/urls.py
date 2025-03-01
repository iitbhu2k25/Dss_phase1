from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdf_list, name='pdf_list'),
    path('pdf/<int:pdf_id>/detail/', views.pdf_detail_api, name='pdf_detail_api'),
    path('pdf/<int:pdf_id>/content/', views.pdf_content, name='pdf_content'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('inspect-db/', views.inspect_database, name='inspect_db'),
]