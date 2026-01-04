from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    """Custom admin for User model with management capabilities"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin_user', 'company_name', 'date_joined', 'is_active')
    list_filter = ('is_admin_user', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'company_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Additional Information'), {
            'fields': ('is_admin_user', 'company_name', 'phone_number', 'shipping_company_name')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Additional Information'), {
            'fields': ('is_admin_user', 'company_name', 'phone_number', 'shipping_company_name')
        }),
    )
    
    def get_queryset(self, request):
        """Only show users that can be managed"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)
    
    def has_delete_permission(self, request, obj=None):
        """Control delete permissions"""
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        """Control change permissions"""
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)


# Register the custom user admin
admin.site.register(User, UserAdmin)

# Customize admin site header and title
admin.site.site_header = 'Ecommerce Inventory Manager Admin'
admin.site.site_title = 'EIM Admin'
admin.site.index_title = 'Admin Dashboard'
