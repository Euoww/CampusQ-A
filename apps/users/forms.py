from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users,Profile
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField # 导入验证码字段

class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'})
    )
    # 添加验证码字段
    captcha = CaptchaField(label='验证码', error_messages={'invalid': '验证码错误'})

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='邮箱')

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 直接从 instance 中获取 user
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user # 从 profile 获取 user
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'placeholder': '请再次输入密码'}))
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'placeholder': '请输入您的用户名'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'placeholder': '请输入您的邮箱地址'}))

    class Meta:
        model = Users
        fields = ['username', 'email']

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('两次密码输入不一致')
        return self.cleaned_data['password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if Users.objects.filter(username=username).exists():
            raise ValidationError('用户名已存在')
        return username
