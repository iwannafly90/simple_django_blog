from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import TagForm, PostForm
from .models import Post, Tag
from .utils import ObjectDetaillMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin


POSTS_PER_PAGE = 1


def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, POSTS_PER_PAGE)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    has_other_pages = page.has_other_pages()
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    context = {
        'page_object': page,
        'has_other_pages': has_other_pages,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'blog_app/index.html', context=context)


class PostDetail(ObjectDetaillMixin, View):
    model = Post
    template = 'blog_app/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog_app/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog_app/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog_app/post_delete_form.html'
    redirect_url = 'post_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog_app/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetaillMixin, View):
    model = Tag
    template = 'blog_app/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog_app/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog_app/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):

    model = Tag
    template = 'blog_app/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True

