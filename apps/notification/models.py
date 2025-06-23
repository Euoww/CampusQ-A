from django.db import models
from apps.users.models import Users

class Notification(models.Model):
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_notifications')
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # 默认按创建时间倒序排列

    def __str__(self):
        return f"To {self.receiver.username}: {self.content}"