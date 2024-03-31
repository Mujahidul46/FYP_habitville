from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    """
    Creates a user model table with custom fields.
    """
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    goals = models.TextField(blank=True, null=True)
    habit_points = models.IntegerField(default=0)  
    life_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Nav bar and main content background colours
    navbar_color = models.CharField(max_length=7, default='#4caf50') # green
    main_content_color = models.CharField(max_length=7, default='#8bc34a') # light green

    def __str__(self):
        return self.username

    def to_dict(self):
        """
        Serializes the user object to a dictionary.
        """
        return {
            'username': self.username,
            'email': self.email,
            'goals': self.goals,
            'habit_points': self.habit_points,  
            'life_points': float(self.life_points),
            'navbar_color': self.navbar_color,
            'main_content_color': self.main_content_color,
        }
    
class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)  
    completed_at = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,  
            'title': self.title,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'completed': self.completed,
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None,
        }
    
    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = now()
        super(ToDo, self).save(*args, **kwargs)

class Habit(models.Model):
    DIFFICULTY_CHOICES = [ # TR, EA, ME, HA shorthand form stored in database
    ('TR', 'Trivial'), 
    ('EA', 'Easy'),
    ('ME', 'Medium'),
    ('HA', 'Hard'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES, default='ME')
    categories = models.ManyToManyField('Category', related_name='habits', blank=True)

    def __str__(self):
        return self.title

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f"{self.habit.title} - {self.date} - {'Completed' if self.completed else 'Not Completed'}"

    def to_dict(self):
        return {
            'habit_id': self.habit.id,
            'date': self.date,
            'completed': self.completed
        }

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.cost} LP"

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
            'notes': self.notes,
            'cost': float(self.cost),
        }

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name