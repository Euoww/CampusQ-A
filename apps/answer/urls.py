# apps/answer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<int:question_id>/add/', views.add_answer, name='add_answer'),
    # 新增的采纳、取消采纳和删除回答的URL
    path('<int:answer_id>/accept/', views.accept_answer, name='accept_answer'),
    path('<int:answer_id>/unaccept/', views.unaccept_answer, name='unaccept_answer'),
    path('<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
]