from django.contrib import admin
from .models import NoticeCategory, Notice, NoticeReadStatus

@admin.register(NoticeCategory)
class NoticeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'is_active', 'is_pinned', 'created_by', 'created_at')
    list_filter = ('category', 'priority', 'is_active', 'is_pinned', 'created_at')
    search_fields = ('title', 'content', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(NoticeReadStatus)
class NoticeReadStatusAdmin(admin.ModelAdmin):
    list_display = ('notice', 'user', 'read_at')
    list_filter = ('read_at',)
    search_fields = ('notice__title', 'user__username')