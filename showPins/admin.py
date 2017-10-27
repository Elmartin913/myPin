from django.contrib import admin
from .models import (
    User,
    Photo,
    Like,
    Comment
)

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email',]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['photo_desc']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['like_type']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment']
