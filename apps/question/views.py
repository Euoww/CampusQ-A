from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, QuestionTag
from ..tag.models import Tag
from .forms import QuestionForm
from django.contrib.auth.decorators import login_required
from apps.comment.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from apps.answer.models import Answer
from apps.comment.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def question_list(request):
    questions_list=Question.objects.all().order_by('-created_at')
    paginator = Paginator(questions_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'question/question_list.html', context)

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.view_count += 1
    question.save()

    # 获取ContentType ID
    question_content_type_id = ContentType.objects.get_for_model(question).id
    answer_content_type_id = ContentType.objects.get_for_model(Answer).id

    comment_form = CommentForm()

    # 对问题评论进行分页
    all_question_comments = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(question),
        object_id=question.pk,
    ).order_by('created_at') # 确保排序，否则分页可能不一致

    comments_per_page = 5 # 每页评论数，可以调整
    paginator = Paginator(all_question_comments, comments_per_page)
    page = request.GET.get('comment_page') # 从URL参数获取页码

    try:
        question_comments = paginator.page(page)
    except PageNotAnInteger:
        question_comments = paginator.page(1) # 如果页码不是整数，则显示第一页
    except EmptyPage:
        question_comments = paginator.page(paginator.num_pages) # 如果页码超出范围，则显示最后一页

    return render(request, 'question/question_detail.html', {
        'question': question,
        'comment_form': comment_form,
        'question_content_type_id': question_content_type_id,
        'answer_content_type_id': answer_content_type_id,
        'question_comments': question_comments, # 传递分页后的评论对象
    })

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 1. 保存 Question 实例（不立即保存到数据库）
            question = form.save(commit=False) # 此时 question 还没有 ID

            # 2. 设置 ForeignKey 字段 author
            question.author = request.user

            # 3. 将 Question 实例保存到数据库，使其获得 ID
            question.save()

            # 4. 现在 question 已经有了 ID，可以处理多对多关系了
            tag_names = form.cleaned_data.get('tags_input', [])
            if tag_names:
                tag_objects = []
                for tag_name in tag_names:
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                    tag_objects.append(tag_obj)
                question.tags.set(tag_objects) # 设置标签

            # 5. 重定向到问题详情页
            return redirect('question_detail', question_id=question.id)
        else:
            print("Form errors:", form.errors) # 打印表单错误以调试
    else:
        form = QuestionForm()
    return render(request, 'question/ask_question.html', {'form': form})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user != question.author:
        return redirect('question_detail', question_id=question.id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question/edit_question.html', {'form': form})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user == question.author:
        question.delete()
        return redirect('question_list')
    return redirect('question_detail', question_id=question.id)
