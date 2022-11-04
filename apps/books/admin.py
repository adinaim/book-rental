from django.contrib import admin
from .models import Post, Tag, Rating, PostImage, Like


admin.site.register([Tag, Rating, Like])


class TabularInLineImages(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ['image']


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [TabularInLineImages]


admin.site.register(Post, PostAdmin)