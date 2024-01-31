from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'goals')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('goals',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'username', 'password1', 'password2', 'goals')}),
    )

admin.site.register(User, UserAdmin)
