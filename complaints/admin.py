from django.contrib import admin
from .models import ComplaintCategory, Complaint, ComplaintUpdate

@admin.register(ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status', 'created_by', 'created_at')
    list_filter = ('category', 'priority', 'status', 'created_at')
    search_fields = ('title', 'created_by__username', 'location')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('complaint__title', 'message')