from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        db_table = 'auth_user'
        fields = ['user_id', 'password1', 'password2']
