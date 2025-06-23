from django.shortcuts import render
from apps.question.models import Question # 导入 Question 模型
from django.db.models import Q # 用于复杂的查询


def search_results(request):
    query = request.GET.get('q') # 获取搜索关键词

    results = Question.objects.none() # 默认空结果集

    if query:
        # 使用 Q 对象进行或 (OR) 查询，搜索标题或内容
        results = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at') # 按创建时间倒序排列

    return render(request, 'search/search_results.html', {
        'query': query,
        'results': results,
    })