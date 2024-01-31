from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_spa, name='main_spa'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login_view'), 
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_api, name='user_api'),  
    path('user/update/', views.update_user_profile, name='update_user_profile'),
]
