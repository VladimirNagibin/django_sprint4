from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>',
        views.CommentDeleteVeiw.as_view(),
        name='delete_comment'
    ),
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts'),
    path(
        'profile/<slug:username>/',
        views.UserPostsListView.as_view(),
        name='profile'
    ),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('edit/', views.PostCreateView.as_view(), name='edit_profile'),
    path('delete/', views.PostCreateView.as_view(), name='delete_post'),
    path(
        'posts/<int:post_id>/comment/',
        views.PostCreateView.as_view(),
        name='add_comment'
    ),
]
