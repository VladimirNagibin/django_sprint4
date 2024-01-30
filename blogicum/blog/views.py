from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse, reverse_lazy

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .constants import POSTS_ON_LIST
from .forms import PostForm
from .models import Category, Post


class PostListView(ListView):
    model = Post
    queryset = Post.objects.get_published_posts()
    # ordering = '-pub_date'
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/index.html'


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.get_published_posts(),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = category.posts.get_published_posts()

    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list}
    )


User = get_user_model()


def profile_user(request, username):
    profile = get_object_or_404(
        User,
        username=username,
    )
    page_obj = profile.posts.get_published_posts()
    return render(
        request,
        'blog/profile.html',
        {'profile': profile, 'page_obj': page_obj}
    )


class UserDetailView(DetailView):
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        context['page_obj'] = self.object.posts.get_published_posts()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)
