# apps/question/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('ask/', views.ask_question, name='ask_question'),
    path('<int:question_id>/', views.question_detail, name='question_detail'),
    path('<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('<int:question_id>/delete/', views.delete_question, name='delete_question'), # <-- Add this line
]