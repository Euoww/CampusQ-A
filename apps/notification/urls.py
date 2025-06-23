from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('read_all/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]
