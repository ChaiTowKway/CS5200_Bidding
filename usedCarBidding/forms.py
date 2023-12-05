from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Car


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name')  # Add other fields if needed


class CustomLoginForm(AuthenticationForm):
    pass  # Customize if needed

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['seller_id']
