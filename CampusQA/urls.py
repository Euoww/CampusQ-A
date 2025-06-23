"""
URL configuration for CampusQA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.search import views

urlpatterns = [
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
    path('', include('apps.question.urls')),           # 首页 = 问题列表
    path('users/', include('apps.users.urls')),
    path('answer/', include('apps.answer.urls')),
    path('comment/', include('apps.comment.urls')),
    path('tag/', include('apps.tag.urls')),
    path('notifications/', include('apps.notification.urls')),
    path('search/', views.search_results, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
