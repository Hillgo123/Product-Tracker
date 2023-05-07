from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Product

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def validate_url(link: str):
    validator = URLValidator()
    try:
        validator(link)

    except ValidationError:
        raise ValidationError('Invalid URL')

class ProductForm(forms.ModelForm):
    link = forms.CharField(validators=[validate_url])

    class Meta:
        model = Product
        fields = ['name', 'link']

class UserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))