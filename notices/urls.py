from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('create/', views.create_notice, name='create_notice'),
    path('<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('<int:notice_id>/edit/', views.edit_notice, name='edit_notice'),
    path('<int:notice_id>/delete/', views.delete_notice, name='delete_notice'),
    path('categories/', views.notice_categories, name='notice_categories'),
    path('categories/create/', views.create_notice_category, name='create_notice_category'),
]