from django.conf.urls import url
from . import views

# 命名空间
app_name = 'blog'
urlpatterns = [
    # 匹配 imzack.me/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 匹配 imzack.me/post/<file>/
    url(r'^post/(?P<file>[0-9a-z-]+).html$', views.PostView.as_view(), name='detail'),
    # 匹配 imzack.me/about.html
    url(r'^about.html$', views.about, name='about'),
]
