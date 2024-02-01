from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User
import json

#TO DO: add comments for each view
def main_spa(request: HttpRequest) -> HttpResponse: 
    if not request.user.is_authenticated:
        return render(request, 'base.html', {
            'welcome_content': True  
        })
    return render(request, 'base.html')


@csrf_exempt
def signup_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('main_spa')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_spa')
    else:
        form = CustomUserCreationForm()

    return render(request, 'api/spa/signup.html', {'form': form})

@csrf_exempt
def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('main_spa')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_spa')
    else:
        form = AuthenticationForm()

    return render(request, 'api/spa/login.html', {'form': form})

@csrf_exempt
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login_view')

@login_required
def user_api(request: HttpRequest) -> JsonResponse:
    """
    Returns the authenticated user's information as JSON.
    """
    if request.method == 'GET':
        return JsonResponse({
            'username': request.user.username,
            'email': request.user.email,
            'goals': request.user.goals
        })
    return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

@login_required
@csrf_exempt
def update_user_profile(request: HttpRequest) -> JsonResponse:
    """
    Updates the authenticated user's profile.
    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = request.user
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.goals = data.get('goals', user.goals)
            user.save()
            return JsonResponse({
                'username': user.username,
                'email': user.email,
                'goals': user.goals
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only PUT method is allowed'}, status=400)
    
def check_authentication(request):
    return JsonResponse({'isAuthenticated': request.user.is_authenticated})
