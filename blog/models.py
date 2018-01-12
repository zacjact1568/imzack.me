from django.db import models
from django.urls import reverse


# 文章类
class Post(models.Model):

    # 标题，存储较短的字符串使用 CharField，设定最长为 50
    title = models.CharField(max_length=50)

    # 文件名
    file = models.CharField(max_length=50)

    # 正文，使用 TextField 来存储大段文本
    content = models.TextField()

    # 日期
    date = models.DateField()

    # 解释器显示的数据为此函数的返回值
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'file': self.file})

    class Meta:
        # 日期逆序（-）排列
        ordering = ['-date']
