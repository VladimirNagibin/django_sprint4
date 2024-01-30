from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from .models import Category, Location, Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'title',
        'description',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'description')
    list_filter = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'author',
        'location',
        'pub_date',
        'is_published'
    )
    list_editable = ('is_published', 'pub_date')
    search_fields = ('title', 'text')
    list_filter = (
        'is_published',
        'category',
        'author',
        'location'
    )


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'posts_count',
        'is_staff'
    )

    @admin.display(description='Кол-во постов у пользователя')
    def posts_count(self, obj):
        return obj.posts.count()
