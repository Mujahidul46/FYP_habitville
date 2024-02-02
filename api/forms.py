from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ToDo

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=25)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

class ToDoForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.Textarea)
    notes = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = ToDo
        fields = ('title', 'notes')

    def __init__(self, *args, **kwargs):
        super(ToDoForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Title'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Notes'})
