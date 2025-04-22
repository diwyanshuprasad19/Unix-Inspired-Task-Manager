from django.contrib import admin
from tasks.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'user', 'created_at', 'updated_at')
    list_filter = ('status', 'user')
    search_fields = ('name', 'user__username')
    ordering = ('-created_at',)
