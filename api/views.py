from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ToDoForm, HabitForm, RewardForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import User, ToDo, Habit, HabitCompletion, Reward, Category, CategoryProgress
import json
from django.middleware.csrf import get_token 
from django.forms.models import model_to_dict
from django.utils.timezone import now
from datetime import datetime
from .points_service import calculate_points
from decimal import Decimal
import math

EXP_REWARD_PER_HABIT = 10

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

@csrf_exempt
@login_required
def user_api(request: HttpRequest) -> JsonResponse:
    """
    Returns the authenticated user's information as JSON.
    """
    if request.method == 'GET':
        user = request.user
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'goals': user.goals,
            'habit_points': user.habit_points,
            'life_points': float(user.life_points),
            'navbar_color': user.navbar_color,
            'main_content_color': user.main_content_color,
        })
    return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

@login_required
@csrf_exempt
def update_user_profile(request: HttpRequest) -> JsonResponse:
    """
    Updates the authenticated user's profile.
    """
    if request.method == 'PUT':
        form = UserProfileForm(data=json.loads(request.body), instance=request.user)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'username': user.username,
                'email': user.email,
                'goals': user.goals,
                'navbar_color': user.navbar_color,
                'main_content_color': user.main_content_color,
            })
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return JsonResponse({'error': 'Only PUT method is allowed'}, status=405)

def check_authentication(request):
    return JsonResponse({'isAuthenticated': request.user.is_authenticated})

@csrf_exempt
@login_required
def create_todo_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = json.loads(request.body)
        form = ToDoForm(data)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            todo_data = model_to_dict(todo)
            return JsonResponse(todo_data, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
@login_required
def list_todo_view(request: HttpRequest) -> HttpResponse:
    todos = ToDo.objects.filter(user=request.user, completed=False).values(
        'id', 'title', 'notes', 'created_at', 'updated_at', 'completed'
    )
    return JsonResponse(list(todos), safe=False)


@csrf_exempt
@login_required
def update_todo_view(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)

    if request.method == 'PUT':
        data = json.loads(request.body)
        form = ToDoForm(data, instance=todo)
        if form.is_valid():
            updated_todo = form.save()
            todo_data = model_to_dict(updated_todo, fields=['id', 'title', 'notes', 'created_at', 'updated_at'])
            return JsonResponse(todo_data, status=200)  
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])
    
@csrf_exempt
@login_required
def delete_todo_view(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'DELETE':
        todo.delete()
        return JsonResponse({'message': 'To Do deleted successfully!'}, status=204)
    else:
        return HttpResponseNotAllowed(['DELETE'])


@csrf_exempt
def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
@login_required
def complete_todo_view(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        completed_status = data.get('completed', False)
        
        todo.completed = completed_status
        if completed_status:
            todo.completed_at = now()
        todo.save(update_fields=['completed', 'completed_at'])
        
        todo_data = model_to_dict(todo, fields=['id', 'title', 'notes', 'created_at', 'updated_at', 'completed', 'completed_at'])
        return JsonResponse(todo_data, status=200)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def list_completed_todos_view(request: HttpRequest) -> HttpResponse:
    completed_todos = ToDo.objects.filter(user=request.user, completed=True)
    todos_data = [model_to_dict(todo, fields=['id', 'title', 'notes', 'created_at', 'updated_at', 'completed', 'completed_at']) for todo in completed_todos]
    return JsonResponse(todos_data, safe=False, status=200)

@csrf_exempt
@login_required
def create_habit_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        notes = data.get('notes', '')
        difficulty = data.get('difficulty', 'ME')
        category_ids = data.get('categories', [])

        if title:
            habit = Habit.objects.create(user=request.user, title=title, notes=notes, difficulty=difficulty)

            if category_ids:
                categories = Category.objects.filter(id__in=category_ids)
                habit.categories.set(categories)

            return JsonResponse({
                'id': habit.id,
                'title': habit.title,
                'notes': habit.notes,
                'difficulty': habit.difficulty,
                'categories': list(habit.categories.values_list('id', flat=True))
            }, status=201)
        else:
            return JsonResponse({'error': 'Title is required.'}, status=400)

@csrf_exempt
@login_required
def list_habits_view(request: HttpRequest) -> HttpResponse: 
    if request.method == 'GET':
        habits = Habit.objects.filter(user=request.user).prefetch_related('categories')
        habit_data = []
        for habit in habits:
            completions = habit.completions.all().values('date', 'completed')  # get completion data for each habit
            category_ids = list(habit.categories.values_list('id', flat=True))
            habit_data.append({
                'id': habit.id,
                'title': habit.title,
                'notes': habit.notes,
                'difficulty': habit.difficulty,
                'categories': category_ids,
                'completions': list(completions),
            })
        return JsonResponse(habit_data, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt
@login_required
def update_habit_completion_view(request: HttpRequest, habit_id: int) -> JsonResponse:
    if request.method == 'PUT':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        data = json.loads(request.body)
        date = data.get('date')
        completed = data.get('completed')
        hp_earned, lp_earned = 0, 0
        
        if date is not None and isinstance(completed, bool):
            date = datetime.strptime(date, '%Y-%m-%d').date()  
            habit_completion, created = HabitCompletion.objects.get_or_create(habit=habit, date=date)
            habit_completion.completed = completed
            
            if completed:
                hp_earned, lp_earned = calculate_points(habit.difficulty) if created or not habit_completion.completed else (0, 0)
                if hp_earned > 0 or lp_earned > 0:
                    request.user.habit_points += hp_earned
                    request.user.life_points += Decimal(lp_earned).quantize(Decimal('0.00'))
                    request.user.save()

                # Update CategoryProgress for each category related to a habit
                for category in habit.categories.all():
                    category_progress, _ = CategoryProgress.objects.get_or_create(user=request.user, category=category)
                    category_progress.current_exp += EXP_REWARD_PER_HABIT 
                    while category_progress.current_exp >= category_progress.exp_to_next_level():
                        category_progress.current_exp -= category_progress.exp_to_next_level()
                        category_progress.level += 1
                    category_progress.save()
                
            habit_completion.save()
            response_data = {
                'habit_id': habit_id,
                'date': date.isoformat(),
                'completed': completed,
                'hp_earned': hp_earned,
                'lp_earned': float(lp_earned),
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'error': 'Date and completed status are required.'}, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])

    
@csrf_exempt
@login_required
def update_habit_view(request: HttpRequest, pk: int) -> HttpResponse:
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        form = HabitForm(data, instance=habit)
        if form.is_valid():
            updated_habit = form.save()
            habit_data = model_to_dict(updated_habit, fields=['id', 'title', 'notes', 'difficulty'])
            habit_data['categories'] = list(updated_habit.categories.values_list('id', flat=True))
            return JsonResponse(habit_data, status=200)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])


@csrf_exempt
@login_required
def delete_habit_view(request: HttpRequest, pk: int) -> HttpResponse: # deletes a habit and all its associated habit completions
    if request.method == 'DELETE':
        habit = get_object_or_404(Habit, pk=pk, user=request.user)  
        habit.delete()  
        return JsonResponse({'message': 'Habit deleted successfully'}, status=204)  
    else:
        return HttpResponseNotAllowed(['DELETE'])


@csrf_exempt
@login_required
def create_reward_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = RewardForm(json.loads(request.body))
        if form.is_valid():
            reward = form.save(commit=False)
            reward.user = request.user
            reward.save()
            return JsonResponse(model_to_dict(reward), status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
@login_required
def list_rewards_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        rewards = Reward.objects.filter(user=request.user).values('id', 'name', 'notes', 'cost')
        return JsonResponse(list(rewards), safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt
@login_required
def spend_reward_view(request: HttpRequest, reward_id: int) -> JsonResponse:
    if request.method == 'POST':
        reward = get_object_or_404(Reward, pk=reward_id, user=request.user)
        if request.user.life_points >= reward.cost:
            request.user.life_points -= reward.cost
            request.user.save(update_fields=['life_points'])
            return JsonResponse({
                'status': 'success',
                'message': 'Reward spent successfully!',
                'new_life_points': float(request.user.life_points)
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Not enough life points to get this reward.'
            }, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])
    
@csrf_exempt
@login_required
def delete_reward_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == 'DELETE':
        reward = get_object_or_404(Reward, pk=pk, user=request.user)  
        reward.delete()  
        return JsonResponse({'message': 'Reward deleted successfully'}, status=204)  
    else:
        return HttpResponseNotAllowed(['DELETE'])

@csrf_exempt
@login_required
def update_reward_view(request: HttpRequest, pk: int) -> JsonResponse:
    reward = get_object_or_404(Reward, pk=pk, user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        form = RewardForm(data, instance=reward)
        if form.is_valid():
            updated_reward = form.save()
            return JsonResponse(updated_reward.to_dict(), status=200)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])

@csrf_exempt   
@login_required
def list_categories_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        categories = Category.objects.all()
        category_data = [{'id': category.id, 'name': category.name} for category in categories]
        return JsonResponse(category_data, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt  
@login_required
def category_progress_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        all_categories = Category.objects.all()
        user_progress_qs = CategoryProgress.objects.filter(user=request.user)

        user_progress_dict = {progress.category.name: progress for progress in user_progress_qs}

        progress_data = []
        for category in all_categories:
            # If user has progress in category, use it
            if category.name in user_progress_dict:
                progress = user_progress_dict[category.name]
                progress_data.append({
                    'category_name': category.name,
                    'level': progress.level,
                    'current_exp': progress.current_exp,
                    'exp_to_next_level': progress.exp_to_next_level(),
                })
            # if user has no exp in a category
            else:
                progress_data.append({
                    'category_name': category.name,
                    'level': 1,
                    'current_exp': 0,
                    'exp_to_next_level': 50,
                })
        
        return JsonResponse(progress_data, safe=False)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
    
@csrf_exempt
@login_required
def spend_habit_points_for_minigame(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        if request.user.habit_points >= 100:
            request.user.habit_points -= 100
            request.user.save(update_fields=['habit_points'])
            return JsonResponse({
                'status': 'success',
                'message': '100 habit points deducted successfully!',
                'new_habit_points': request.user.habit_points
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Not enough habit points to play the minigame.'
            }, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])