from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_spa, name='main_spa'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_api, name='user_api'),
    path('user/update/', views.update_user_profile, name='update_user_profile'),
    path('check_authentication/', views.check_authentication, name='check_authentication'),
    path('create-todo/', views.create_todo_view, name='create_todo'),
    path('list-todo/', views.list_todo_view, name='list_todo'),
    path('csrf/', views.csrf, name='csrf'),
    path('update-todo/<int:pk>/', views.update_todo_view, name='update_todo'),
    path('delete-todo/<int:pk>/', views.delete_todo_view, name='delete_todo'),
    path('mark-completed/<int:pk>/', views.complete_todo_view, name='mark_todo_completed'),
    path('list-completed/', views.list_completed_todos_view, name='list_completed_todos'),
    path('create-habit/', views.create_habit_view, name='create_habit'),
    path('list-habits/', views.list_habits_view, name='list_habits'),
    path('update-habit-completion/<int:habit_id>/', views.update_habit_completion_view, name='update_habit_completion'),
    path('update-habit/<int:pk>/', views.update_habit_view, name='update_habit'),
]
