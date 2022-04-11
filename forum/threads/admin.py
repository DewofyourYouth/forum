from django.contrib import admin
from threads.models import Thread, User

# Register your models here.
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "created_by"]
