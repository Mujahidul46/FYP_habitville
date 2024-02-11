from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ToDo, Habit, HabitCompletion

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'goals', 'habit_points', 'life_points')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('goals', 'habit_points', 'life_points')}),
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
    
class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'difficulty', 'notes') 
    list_filter = ('user', 'difficulty') 
    search_fields = ('title', 'notes')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'completed')
    list_filter = ('habit', 'date', 'completed')
    search_fields = ('habit__title', 'date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(habit__user=request.user)
    
admin.site.register(User, UserAdmin)
admin.site.register(ToDo, ToDoAdmin)
admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitCompletion, HabitCompletionAdmin)
