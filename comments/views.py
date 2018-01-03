from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .forms import CommentForm


def post_comment(request, post_pk):

    post = get_object_or_404(Post, pk=post_pk)

    # 只有当请求为 post 时才需要处理表单数据
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中
        form = CommentForm(request.POST)

        # 检查表单数据是否符合格式要求
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来
            comment.post = post

            # 将评论数据保存进数据库
            comment.save()

            # 重定向到 post 的详情页
            # 当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，然后重定向到 get_absolute_url 方法返回的 URL
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误
            # 传了三个模板变量给 detail.html，一个是文章（Post），一个是评论列表，一个是表单 form
            # 使用 post.comment_set.all() 获取这篇 post 下的的全部评论，等价于 Comment.objects.filter(post=post)
            # 因为 Post 和 Comment 是外键关联的，因此也可以使用 post.comment_set.all() 反向查询全部评论
            comment_list = post.comment_set.all()
            context = {'post': post, 'form': form, 'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)
