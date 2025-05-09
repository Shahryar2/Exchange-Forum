from msilib.schema import ListView
from django.contrib.auth.views import  LoginView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import PostForm
from .forms import ProfileForm
from .models import Post,Profile,Comment
from .forms import SignUpForm
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models

# Create your views here.
def index(request):
    # 获取筛选参数
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')
    
    # 基础查询集
    posts = Post.objects.all()
    
    # 应用搜索
    if search_query:
        posts = posts.filter(
            models.Q(title__icontains=search_query) |
            models.Q(content__icontains=search_query)
        )
    
    # 应用筛选
    if filter_type == 'hot':
        # 获取评论最多的帖子
        posts = posts.annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count', '-created_date')
    elif filter_type == 'new':
        # 最新帖子
        posts = posts.order_by('-created_date')
    elif filter_type == 'my' and request.user.is_authenticated:
        # 我的帖子
        posts = posts.filter(author=request.user).order_by('-created_date')
    else:
        # 默认按创建时间排序
        posts = posts.order_by('-created_date')
    
    # 获取论坛统计数据
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    
    # 获取活跃用户（过去30天内发帖最多的用户）
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = User.objects.annotate(
        post_count=Count('post', filter=models.Q(post__created_date__gte=thirty_days_ago))
    ).order_by('-post_count')[:5]
    
    context = {
        'posts': posts,
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'active_users': active_users,
        'filter_type': filter_type,
        'search_query': search_query,
    }
    return render(request, '学术交流/index.html', context)

def post_list(request):
    """显示所有帖子的列表视图"""
    posts = Post.objects.all().order_by('-created_date')
    return render(request, '学术交流/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """显示单个帖子的详细信息视图"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('comment_content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
    return render(request, '学术交流/post_detail.html', {'post': post})

#创建新帖子
#@login_required(login_url='/login/')
def create_post(request):
    print("Create post view called")
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            print("form is valid")
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'学术交流/post_create.html',{'form':form})

#注册视图
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #is_valid()函数来验证表单数据是否有效，处理用户提交表单数据前，先对其有效性进行验证
        if form.is_valid():
            user = form.save()
            # Profile会通过信号自动创建，不需要在这里手动创建
            redirect_url = request.build_absolute_uri(reverse('login'))+'?register_success=True'
            return HttpResponseRedirect(redirect_url) #注册成功后重定向到帖子的列表页面，并携带成功消息
        else:
            #如果表单不合法，将错误信息传递给模块
            return render(request,'学术交流/register.html',{'form':form,'success':False})
    else:
         form = SignUpForm()
    return render(request,'学术交流/register.html',{'form':form,'success':None})

#登陆视图
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 由于使用了信号，确保在访问之前 Profile 已经创建
            user.profile = Profile.objects.get_or_create(user=user)[0]
            login(request, user)
            return HttpResponseRedirect(reverse('home'))  # 替换为实际的登录成功页面
        else:
            return HttpResponseRedirect('/login-error/')  # 替换为实际的错误提示页面
    else:
        return render(request, '学术交流/login.html')

def login_error(request):
    return render(request, '学术交流/login_error.html')

#登出视图
def user_logout(request):
    logout(request)
    return redirect('post_list')

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    # 获取用户的帖子和评论
    user_posts = Post.objects.filter(author=request.user).order_by('-created_date')
    user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'form': form,
        'user_posts': user_posts,
        'user_comments': user_comments,
    }
    return render(request, '学术交流/profile.html', context)

#在登录界面的视图中检查是否有一个成功的注册，如果是，就显示成功消息
from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name = '学术交流/templates/login.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['username']=self.request.GET.get('register_success')=='True'
        return context

def update_profile(request):
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile = request.user.profile
        profile.bio = bio
        profile.save()
        return redirect('profile')
    return redirect('profile')

def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = request.user.profile
        profile.avatar = request.FILES['avatar']
        profile.save()
    return redirect('profile')

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('post_list')