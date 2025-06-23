# apps/answer/models.py
from django.db import models
from apps.question.models import Question
from apps.users.models import Users
from django.contrib.contenttypes.fields import GenericRelation # 导入 GenericRelation

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    comments = GenericRelation('comment.Comment') # 反向关联到 Comment 模型

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.username}"