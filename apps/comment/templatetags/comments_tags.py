# apps/comment/templatetags/comments_tags.py
from django import template
from django.contrib.contenttypes.models import ContentType
from apps.comment.models import Comment

register = template.Library()

@register.simple_tag
def get_comments_for_object(obj):
    """
    Retrieves all comments for a given object.
    Usage: {% get_comments_for_object some_object as comments_list %}
    """
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk)