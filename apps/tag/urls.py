from django.urls import path
from . import views

urlpatterns = [
    path('<int:tag_name>/questions/', views.questions_by_tag, name='questions_by_tag'),
]
