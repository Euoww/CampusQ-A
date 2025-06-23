from django import forms
from .models import Question, Tag
from django.core.exceptions import ValidationError

class QuestionForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='标签（用空格分隔）',
        required=False,
        help_text='输入多个标签，用空格分隔。'
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'is_anonymous']
        # 移除 tags 的 widget 设置，因为我们现在用 tags_input 处理
        # widgets = {
        #     'tags': forms.CheckboxSelectMultiple
        # }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tags_input'] = ' '.join([tag.name for tag in self.instance.tags.all()])

    def clean_tags_input(self):
        tags_data = self.cleaned_data['tags_input']
        if tags_data:
            tag_names = [name.strip() for name in tags_data.split(' ') if name.strip()]
            return tag_names
        return []

    # 关键修改在这里
    def save(self, commit=True):
        # 1. 首先保存 Question 实例，使其获得 ID
        question = super().save(commit=False) # 获取Question实例，但不立即保存
        # 这里不能直接调用 question.save()，因为我们还没有设置 author
        # question.author 的设置是在 views.py 中完成的

        # 2. 如果 commit=True，Django 默认会保存 M2M 字段
        # 但由于我们自定义了 tags_input，需要手动处理 M2M 关系

        # 我们将 M2M 关系的保存推迟到视图函数中，
        # 因为 question.author 是在视图中设置的，并且需要在 question 保存后才能处理 tags。
        # 因此，在这里我们只处理非 M2M 字段的保存。
        if commit:
            question.save() # 确保 question 有 ID

        # 3. 返回 question 实例，让视图函数继续处理
        return question

