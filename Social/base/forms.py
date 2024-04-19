from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class MyUserCreationForm(UserCreationForm):
    """User registration form."""

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']



class RoomForm(ModelForm):
    """Room creation form by users."""

    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']



class UserForm(ModelForm):
    """There is an update form for users who have already registered."""

    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']