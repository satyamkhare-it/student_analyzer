from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analyzer/', views.upload_file, name='upload'),
]
