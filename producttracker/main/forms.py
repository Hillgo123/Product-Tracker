from collections import OrderedDict
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
    valid_urls = [
        'https://www.netonnet.se', 
        'https://www.mediamarkt.se', 
        'https://www.inet.se'
        ]
    
    for i in valid_urls:
        if link.startswith(i):
            validator(link)

        else:
            raise ValidationError('Invalid URL; Current Valid URLs: https://www.netonnet.se \n https://www.mediamarkt.se \n https://www.inet.se')
            

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
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
        label="Old password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
        label="New password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
        label="Confirm new password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reorder fields from new_password1, new_password2, old_password to old_password, new_password1, new_password2
        self.fields = OrderedDict([
            ('old_password', self.fields['old_password']),
            ('new_password1', self.fields['new_password1']),
            ('new_password2', self.fields['new_password2']),
        ])

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)