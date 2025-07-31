from django.contrib import admin
from .models import Meeting, MeetingAttendance, MeetingDocument

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('title', 'location', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MeetingAttendance)
class MeetingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'user', 'response', 'attended', 'created_at')
    list_filter = ('response', 'attended', 'created_at')
    search_fields = ('meeting__title', 'user__username')

@admin.register(MeetingDocument)
class MeetingDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'meeting', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('title', 'meeting__title')