from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
    path('create/', views.create_complaint, name='create_complaint'),
    path('<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
]