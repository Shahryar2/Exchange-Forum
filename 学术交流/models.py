# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

#Post模型代表博客帖子
class Post(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    #使用外键类型，帖子和用户关联
    text=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

#代表评论
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

#储存用户资料
class Profile(models.Model):
    #建立与User模型的一对一关联
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #用于储存个人简介
    bio=models.TextField(blank=True)
    #用于储存用户上传的头像图片
    avatar=models.ImageField(upload_to='profile/',blank=True)
    #返回关联的用户名
    def __str__(self):
        return self.user.username

#定义一个信号处理器
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)