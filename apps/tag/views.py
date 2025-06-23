# apps/tag/views.py
from django.shortcuts import render, get_object_or_404
from .models import Tag  # 确保导入 Tag 模型
from apps.question.models import Question  # 导入 Question 模型


def questions_by_tag(request, tag_name):
    # 根据 tag_pk 获取标签对象，如果不存在则返回 404
    tag = get_object_or_404(Tag, pk=tag_name)
    # 获取所有与该标签关联的问题，并按创建时间倒序排列
    # Django 的 ManyToManyField 允许直接通过关联对象进行过滤
    questions = Question.objects.filter(tags=tag).order_by('-created_at')

    return render(request, 'tag/questions_by_tag.html', {
        'tag': tag,  # 将标签对象传递给模板
        'questions': questions,  # 将查询到的问题列表传递给模板
    })

# （可选）如果你需要一个显示所有标签的页面，可以添加这个视图
# def tag_list(request):
#     tags = Tag.objects.all().order_by('name')
#     return render(request, 'tag/tag_list.html', {'tags': tags})