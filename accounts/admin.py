from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Society

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'flat_number', 'wing', 'is_verified', 'is_active')
    list_filter = ('user_type', 'is_verified', 'is_active', 'wing')
    search_fields = ('username', 'email', 'flat_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'flat_number', 'wing', 'emergency_contact', 'profile_picture', 'is_verified')
        }),
    )

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'total_flats', 'contact_email', 'established_date')
    search_fields = ('name', 'registration_number')