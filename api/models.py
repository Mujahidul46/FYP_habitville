from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    """
    Creates a user model table with custom fields for Habitville app.
    """
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    goals = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

    def to_dict(self):
        """
        Serializes the user object to a dictionary.
        """
        return {
            'username': self.username,
            'email': self.email,
            'goals': self.goals
        }
    
class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        }
