from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ToDo

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'goals')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('goals',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'username', 'password1', 'password2', 'goals')}),
    )

class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'completed', 'completed_at')
    list_filter = ('created_at', 'user', 'completed')
    search_fields = ('title', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')  

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(User, UserAdmin)
admin.site.register(ToDo, ToDoAdmin)
