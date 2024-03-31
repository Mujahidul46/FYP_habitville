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
    path('delete-habit/<int:pk>/', views.delete_habit_view, name='delete_habit'),
    path('create-reward/', views.create_reward_view, name='create_reward'),
    path('list-rewards/', views.list_rewards_view, name='list_rewards'),
    path('spend-reward/<int:reward_id>/', views.spend_reward_view, name='spend_reward'),
    path('delete-reward/<int:pk>/', views.delete_reward_view, name='delete_reward'),
    path('update-reward/<int:pk>/', views.update_reward_view, name='update_reward'),
    path('list-categories/', views.list_categories_view, name='list_categories'),
    path('category-progress/', views.category_progress_view, name='category_progress_view'),
]
