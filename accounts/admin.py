from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Society

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'society', 'flat_number', 'wing', 'is_verified', 'is_active')
    list_filter = ('user_type', 'society', 'is_verified', 'is_active', 'wing')
    search_fields = ('username', 'email', 'flat_number', 'society__name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'society', 'phone', 'flat_number', 'wing', 'emergency_contact', 'profile_picture', 'is_verified')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # If user has a society, only show users from same society
        if hasattr(request.user, 'society') and request.user.society:
            return qs.filter(society=request.user.society)
        return qs.none()

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'total_flats', 'contact_email', 'established_date')
    search_fields = ('name', 'registration_number')