from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_list, name='record_list'),  # home page of scraper app
    path('record/<int:pk>/', views.record_detail, name='record_detail'),  # detail page
    path('records/', views.records_list, name='records_list'),  # records list page
]
