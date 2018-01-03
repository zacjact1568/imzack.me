import markdown
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from comments.forms import CommentForm
from .models import Post


def index(request):
    post_list = Post.objects.all()
    # 生成摘要
    for post in post_list:
        excerpt_index = post.content.find('<!--more-->')
        if excerpt_index > -1:
            # 若在正文中找到 <!--more-->，将其前面部分作为摘要
            post.excerpt = post.content[:excerpt_index]
        else:
            # 否则使用全部正文作为摘要
            post.excerpt = post.content
        post.excerpt = markdown.markdown(post.excerpt)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, file):
    post = get_object_or_404(Post, file=file)
    post.content = markdown.markdown(post.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      # 语法高亮
                                      'markdown.extensions.codehilite',
                                      # 自动生成目录
                                      'markdown.extensions.toc',
                                     ])
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    context = {'post': post, 'form': form, 'comment_list': comment_list}
    return render(request, 'blog/detail.html', context=context)


class IndexView(ListView):
    # 要获取的模型
    model = Post
    # 指定视图渲染的模板
    template_name = 'blog/index.html'
    # 指定获取的模型列表数据保存的变量名，此变量会被传递给模板
    context_object_name = 'post_list'
    # 指定每一页包含的文章数量
    paginate_by = 5

    def get_queryset(self):
        post_list = super(IndexView, self).get_queryset()
        # 生成摘要
        for post in post_list:
            excerpt_index = post.content.find('<!--more-->')
            if excerpt_index > -1:
                # 若在正文中找到 <!--more-->，将其前面部分作为摘要
                # 动态为 post 添加 excerpt 属性
                post.excerpt = post.content[:excerpt_index]
            else:
                # 否则使用全部正文作为摘要
                post.excerpt = post.content
            post.excerpt = markdown.markdown(post.excerpt)
        return post_list

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        # 获取父类生成的字典的模板变量
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context

    # 获取显示分页导航条需要的数据
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    # 指定 URL 中模板的参数
    slug_url_kwarg = 'file'
    # 指定 Post 中哪个字段对应 URL 中模板的参数
    slug_field = 'file'

    def get_object(self, queryset=None):
        # 对 content 进行 markdown 渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            # 语法高亮
            'markdown.extensions.codehilite',
            # 自动生成目录
            TocExtension(slugify=slugify),
        ])
        post.content = md.convert(post.content)
        # 添加 markdown.extensions.toc 扩展后，md 就会多出一个 toc 属性
        # 动态为 post 添加 toc 属性
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 将评论列表和表单传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        # 获取这篇 post 下的全部评论
        comment_list = self.object.comment_set.all()
        context.update({'form': form, 'comment_list': comment_list})
        return context


def about(request):
    return render(request, 'blog/about.html')
