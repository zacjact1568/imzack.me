from django.db import models


# 评论类
class Comment(models.Model):

    name = models.CharField(max_length=50)

    # 个人网站
    website = models.URLField(blank=True)

    # 内容
    content = models.TextField()

    # auto_now_add：当评论保存到数据库时，自动把指定为当前时间
    time = models.DateTimeField(auto_now_add=True)

    # 评论属于哪篇文章
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.content[:20]
