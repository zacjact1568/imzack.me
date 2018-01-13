from django.db import models


# 评论类
class Comment(models.Model):

    # 名字
    name = models.CharField('名字', max_length=50)

    # 网站
    website = models.URLField('网站', blank=True)

    # 内容
    content = models.TextField('评论')

    # auto_now_add：当评论保存到数据库时，自动把指定为当前时间
    time = models.DateTimeField('时间', auto_now_add=True)

    # 评论属于哪篇文章
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, verbose_name='文章')

    def __str__(self):
        return self.content[:20]

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
