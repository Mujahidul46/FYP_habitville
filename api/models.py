from django.db import models
from django.contrib.auth.models import AbstractUser

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
