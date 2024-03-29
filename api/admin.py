from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ToDo, Habit, HabitCompletion, Reward, Category

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'goals', 'habit_points', 'life_points', 'navbar_color', 'main_content_color')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('goals', 'habit_points', 'life_points', 'navbar_color', 'main_content_color' )}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'username', 'password1', 'password2', 'goals', 'navbar_color', 'main_content_color')}),
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
    list_display = ('title', 'user', 'difficulty', 'get_categories', 'notes') 
    list_filter = ('user', 'difficulty') 
    search_fields = ('title', 'notes')

    def get_categories(self, obj):
        """Returns categories of a habit as a comma-separated list."""
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

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
    
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'user', 'notes')
    list_filter = ('user',)
    search_fields = ('name', 'notes', 'cost')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
admin.site.register(User, UserAdmin)
admin.site.register(ToDo, ToDoAdmin)
admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitCompletion, HabitCompletionAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Category, CategoryAdmin)