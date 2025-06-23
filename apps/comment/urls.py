from django.urls import path
from . import views

urlpatterns = [
    path('<int:content_type_id>/<int:object_id>/add/', views.add_comment, name='add_comment'),
    path('delete/<int:pk>/', views.delete_comment, name='delete_comment'), # 新增删除评论URL
]