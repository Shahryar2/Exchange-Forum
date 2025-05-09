from django.urls import path
from . import views
from .views import index,profile
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('post_list/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update_avatar/', views.update_avatar, name='update_avatar'),
    path('login-error/', views.login_error, name='login_error'),
]

#分别对应帖子列表页面，单个帖子的详情页面以及创建新帖子的页面,注册页面，登录页面以及登出页面
#每个path（）包含一个URL路径，一个视图函数，一个唯一的名称
#通过以上Django可以根据请求的URL来确定应该调用哪个视图函数
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#通过Web服务器提供媒体文件服务,将媒体文件路径和URL绑定在一起