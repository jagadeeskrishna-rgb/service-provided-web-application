from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "address", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.CUSTOMER
        if commit:
            user.save()
        return user

class ProviderRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "address", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.PROVIDER
        if commit:
            user.save()
        return user
