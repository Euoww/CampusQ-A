
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from apps.users.forms import LoginForm,RegisterForm,ProfileForm
from apps.users.models import Users, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = Users.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)  # 注册成功后直接登录
            return redirect('question_list')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})

# 登录

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) # 使用你自定义的 LoginForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # authenticate() 在 Django 2.0+ 推荐传入 request 对象
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # 登录成功后跳转到首页或其他指定页面
                # 请确保你在 urls.py 中为这个 URL 模式定义了 name='question_list'
                return redirect('question_list')
            else:
                # 认证失败时，向表单添加一个非字段错误
                form.add_error(None, '用户名或密码错误')
        # 如果表单本身就无效（比如字段没有通过验证规则）
        # form.errors 会自动包含这些错误信息
    else:
        form = LoginForm() # GET 请求时初始化一个空表单

    return render(request, 'user/login.html', {'form': form})

# 登出

def user_logout(request):
    logout(request) # 执行登出操作
    return redirect('question_list') # 或者 redirect('home')

# 用户个人主页
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request, user_id): # <-- user_id 在这里被接收
    # 确保 user_id 与当前登录用户匹配，防止用户访问他人主页
    if user_id != request.user.id:
        return redirect('profile', user_id=request.user.id) # 重定向到自己的主页

    # 获取当前登录用户的 Profile
    # 注意：这里可以直接使用 request.user.profile，因为 OneToOneField 会自动创建反向关联
    # 也可以更安全地获取：
    profile = get_object_or_404(Profile, user=request.user) # 确保获取的是当前用户的Profile

    if request.method == 'POST':
        # form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        # 优化：ProfileForm已经可以直接从instance获取user，所以user=request.user可以移除
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # ！！关键修改在这里！！
            return redirect('profile', user_id=request.user.id) # 提供 user_id 参数
    else:
        # form = ProfileForm(instance=profile, user=request.user)
        form = ProfileForm(instance=profile) # 同理，移除user=request.user
    return render(request, 'user/profile.html', {'form': form})



@receiver(post_save, sender=Users)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# 编辑个人信息
def edit_profile(request):
    pass
