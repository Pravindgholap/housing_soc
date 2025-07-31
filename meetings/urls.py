from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
    path('create/', views.create_meeting, name='create_meeting'),
    path('<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
    path('<int:meeting_id>/status/', views.update_meeting_status, name='update_meeting_status'),
]