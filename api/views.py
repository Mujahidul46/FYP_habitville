from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ToDoForm, HabitForm
from django.contrib.auth.decorators import login_required
from .models import User, ToDo, Habit, HabitCompletion
import json
from django.middleware.csrf import get_token 
from django.forms.models import model_to_dict
from django.utils.timezone import now
from datetime import datetime
from .points_service import calculate_points
from decimal import Decimal


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
            'goals': request.user.goals,
            'habit_points': request.user.habit_points,  
            'life_points': float(request.user.life_points),  
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
        if title:  
            habit = Habit.objects.create(user=request.user, title=title, notes=notes, difficulty=difficulty)
            return JsonResponse({
                'id': habit.id, 
                'title': habit.title, 
                'notes': habit.notes, 
                'difficulty': habit.difficulty
            }, status=201)
        else: 
            return JsonResponse({'error': 'Title is required.'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
@login_required
def list_habits_view(request: HttpRequest) -> HttpResponse: 
    if request.method == 'GET':
        habits = Habit.objects.filter(user=request.user)
        habit_data = []
        for habit in habits:
            completions = habit.completions.all().values('date', 'completed') # get completion data for each habit
            habit_data.append({
                'id': habit.id,
                'title': habit.title,
                'notes': habit.notes,
                'difficulty': habit.difficulty,  
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
        
        if date is not None and isinstance(completed, bool):
            date = datetime.strptime(date, '%Y-%m-%d').date()  
            habit_completion, created = HabitCompletion.objects.get_or_create(habit=habit, date=date)
            habit_completion.completed = completed
            
            if completed and created:
                hp_earned, lp_earned = calculate_points(habit.difficulty)
                request.user.habit_points += hp_earned
                request.user.life_points += Decimal(lp_earned).quantize(Decimal('0.00'))
                request.user.save()
                
            habit_completion.save()
            response_data = {
                'habit_id': habit_id,
                'date': date.isoformat(),
                'completed': completed,
                'hp_earned': hp_earned if completed and created else 0,
                'lp_earned': float(lp_earned) if completed and created else 0.00,
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
