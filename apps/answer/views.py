from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Answer
from ..question.models import Question
from ..notification.models import Notification
from .forms import AnswerForm
from django.contrib.auth.decorators import login_required

@login_required
def add_answer(request, question_id): # 接收 question_id 参数
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question # 设置关联的问题
            answer.author = request.user # 设置回答者
            answer.save()
            # 可添加通知逻辑
            messages.success(request, '回答成功！')
            return redirect('question_detail', question_id=question.id) # 回答后重定向回问题详情页
        else:
            # 如果表单无效，可能需要重新渲染问题详情页，并显示表单错误
            print("Answer form errors:", form.errors)
            # return render(request, 'question/question_detail.html', {'question': question, 'answers': question.answers.all(), 'form': form})
            # 简化处理，直接重定向（但用户看不到错误）
            return redirect('question_detail', question_id=question.id)
    # 如果是GET请求访问这个URL，通常不直接在这里渲染表单
    return redirect('question_detail', question_id=question.id)


@login_required
def accept_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    # 确保当前用户是问题的作者
    if request.user == answer.question.author:
        # 先取消其他已采纳的回答（每个问题只能有一个最佳回答）
        Answer.objects.filter(question=answer.question, is_accepted=True).update(is_accepted=False)
        answer.is_accepted = True
        answer.save()
        messages.success(request, '回答已采纳！')
    else:
        messages.error(request, '您无权采纳此回答。')
    return redirect('question_detail', question_id=answer.question.id)

@login_required
def unaccept_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    # 确保当前用户是问题的作者
    if request.user == answer.question.author:
        answer.is_accepted = False
        answer.save()
        messages.success(request, '已取消采纳此回答。')
    else:
        messages.error(request, '您无权取消采纳此回答。')
    return redirect('question_detail', question_id=answer.question.id)

@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question_id = answer.question.id # 记录问题ID以便重定向

    # 判断是否有权限删除：问题的作者 或 回答者本人
    if request.user == answer.question.author or request.user == answer.author:
        answer.delete()
        messages.success(request, '回答已删除！')
        # 如果问题的所有回答都被删除了，采纳状态也需要重置
        if not answer.question.answers.exists():
            answer.question.is_accepted = False # 假设问题模型有这个字段
            answer.question.save()
    else:
        messages.error(request, '您无权删除此回答。')
    return redirect('question_detail', question_id=question_id)

@login_required
def add_answer_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()

            # ！！生成通知！！
            # 只有当回答者不是问题发布者时才发送通知
            if request.user != question.author:
                Notification.objects.create(
                    receiver=question.author, # 通知问题的作者
                    sender=request.user,     # 回答者是发送者
                    content=f"您的提问 '{question.title}' 有了新回答！"
                )
                messages.success(request, '回答成功并通知了问题发布者！')
            else:
                messages.success(request, '回答成功！')

            return redirect('question_detail', question_id=question.id)
        else:
            print("Answer form errors:", form.errors)
            messages.error(request, '提交回答失败，请检查。') # 添加错误提示
            return redirect('question_detail', question_id=question.id) # 也可以重新渲染页面显示错误
    return redirect('question_detail', question_id=question.id)

@login_required
def accept_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user == answer.question.author:
        # 先取消其他已采纳的回答
        Answer.objects.filter(question=answer.question, is_accepted=True).update(is_accepted=False)
        answer.is_accepted = True
        answer.save()

        # ！！生成通知！！
        # 通知被采纳回答的作者
        Notification.objects.create(
            receiver=answer.author, # 通知回答的作者
            sender=request.user,     # 问题的作者是发送者
            content=f"您的回答在 '{answer.question.title}' 问题中被采纳了！"
        )
        messages.success(request, '回答已采纳！并通知了回答者。')
    else:
        messages.error(request, '您无权采纳此回答。')
    return redirect('question_detail', question_id=answer.question.id)