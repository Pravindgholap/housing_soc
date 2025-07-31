from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.bill_list, name='bill_list'),
    path('create/', views.create_bill, name='create_bill'),
    path('bill/<int:bill_id>/', views.bill_detail, name='bill_detail'),
    path('bill/<int:bill_id>/payment/', views.make_payment, name='make_payment'),
    path('bill/<int:bill_id>/receipt/', views.generate_receipt, name='generate_receipt'),
    path('types/', views.maintenance_types, name='maintenance_types'),
    path('types/create/', views.create_maintenance_type, name='create_maintenance_type'),
]