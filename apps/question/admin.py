from django.contrib import admin
from .models import Question, QuestionTag

admin.site.register(Question)
admin.site.register(QuestionTag)
