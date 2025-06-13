# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('find-job',views.find_job,name='find_job'),
    path('create-job/', views.job_create, name='job_create'),
]
