from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


def post_list(request):
    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer return the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If out range return last page
        posts = paginator.page(paginator.num_pages)

    return render(request,
                   'main/post/list.html',
                     {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                              status=Post.Status.PUBLISHED,
                                slug=post,
                                  publish__year=year,
                                    publish__month=month,
                                      publish__day=day)

    return render(request,
                   'main/post/detail.html',
                     {'post': post})







