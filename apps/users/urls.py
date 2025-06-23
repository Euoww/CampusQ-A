from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

]