# apps/question/models.py
from django.db import models
from apps.users.models import Users
from apps.tag.models import Tag
from django.contrib.contenttypes.fields import GenericRelation # 导入 GenericRelation

class Question(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False, verbose_name='匿名提问')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, through='QuestionTag')
    comments = GenericRelation('comment.Comment') # <-- 添加这行，反向关联到 Comment 模型

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)