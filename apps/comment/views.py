# apps/comment/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm
from apps.question.models import Question  # 导入 Question 模型，用于重定向
from apps.answer.models import Answer  # 导入 Answer 模型，用于重定向
from apps.notification.models import Notification  # 导入 Notification 模型，用于生成通知

@login_required
def add_comment(request, content_type_id, object_id):
    try:
        model_class = ContentType.objects.get_for_id(content_type_id).model_class()
        content_object = get_object_or_404(model_class, pk=object_id)
    except Exception:
        messages.error(request, '评论对象不存在或类型错误。')
        return redirect('question_list')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_type = ContentType.objects.get_for_model(content_object)
            comment.object_id = content_object.pk
            comment.author = request.user
            comment.save()

            # !! IMPORTANT FIX: Define content_type_name and item_title BEFORE the if/else for notification !!
            content_type_name = "问题" if isinstance(content_object, Question) else "回答"
            # Adjust item_title logic to handle both Question and Answer
            if isinstance(content_object, Question):
                item_title = content_object.title
            elif isinstance(content_object, Answer):
                item_title = content_object.question.title # Get the title of the question the answer belongs to
            else:
                item_title = "未知内容" # Fallback for unexpected content_object types


            if request.user != content_object.author:
                Notification.objects.create(
                    receiver=content_object.author,
                    sender=request.user,
                    content=f"您的{content_type_name} '{item_title}' 收到了一条新评论！"
                )
                messages.success(request, f'成功评论{content_type_name}并通知了作者！')
            else:
                messages.success(request, f'成功评论{content_type_name}！')

            # Redirection logic
            if isinstance(content_object, Question):
                return redirect('question_detail', question_id=content_object.pk)
            elif isinstance(content_object, Answer):
                return redirect('question_detail', question_id=content_object.question.pk)
        else:
            messages.error(request, '评论提交失败，请检查内容。')

    # Redirection for GET requests or invalid form (if any)
    if isinstance(content_object, Question):
        return redirect('question_detail', question_id=content_object.pk)
    elif isinstance(content_object, Answer):
        return redirect('question_detail', question_id=content_object.question.pk)
    return redirect('question_list')

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # 获取评论所属的问题ID，以便删除后重定向
    question_id = None
    if isinstance(comment.content_object, Question):
        question_id = comment.content_object.pk
    elif isinstance(comment.content_object, Answer):
        question_id = comment.content_object.question.pk

    # 权限检查：评论作者本人 或 问题/回答的作者 或 管理员
    # 为了简化，这里只检查评论作者和问题/回答作者
    can_delete = False
    if request.user == comment.author: # 评论作者可以删除自己的评论
        can_delete = True
    # 如果评论是对问题的，检查当前用户是否是问题作者
    elif isinstance(comment.content_object, Question) and request.user == comment.content_object.author:
        can_delete = True
    # 如果评论是对回答的，检查当前用户是否是回答的作者
    elif isinstance(comment.content_object, Answer) and request.user == comment.content_object.author:
        can_delete = True
    # 还可以添加：elif request.user.is_staff: # 管理员权限

    if can_delete:
        comment.delete()
        messages.success(request, '评论已删除！')
    else:
        messages.error(request, '您无权删除此评论。')

    if question_id:
        return redirect('question_detail', question_id=question_id)
    return redirect('question_list') # 极端情况，如果获取不到问题ID，重定向到问题列表