from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FileUpload

# Custom admin for User model
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

# Admin for file uploads
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'uploaded_at')
    list_filter = ('content_type', 'uploaded_at')
    search_fields = ('user__username',)
    readonly_fields = ('file', 'content_type', 'uploaded_at')

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(FileUpload, FileUploadAdmin)