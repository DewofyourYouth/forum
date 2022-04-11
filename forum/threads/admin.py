from django.contrib import admin
from threads.models import Thread, Comment

# Register your models here.
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "created_at", "created_by"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "thread", "user", "created_at", "title", "content"]
