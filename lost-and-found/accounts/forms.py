from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class SignupForm(UserCreationForm):
    ALLOWED_EMAILS = {
        "vrsec.ac.in", "iiti.ac.in", "pesu.pes.edu", "vnrvjiet.in"  # Add more institutional domains
    }
    TEAM_EMAILS = {
        "dnandinich@gmail.com", "mishajain1110@gmail.com", "praneethakalbhavi@gmail.com", "sirivoore249@gmail.com"
    }

    username = forms.CharField(
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Username'}),
        label = 'Roll Number'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        max_length=32,
        label = 'First Name'

    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        max_length=32,
        label='Last Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        max_length=64,
        label='Email'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]

        if domain not in self.ALLOWED_EMAILS and email not in self.TEAM_EMAILS:
            raise ValidationError("Only institutional or team member emails are allowed.")

        return email
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label='Old Password'
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='New Password'
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

class EditProfileForm(forms.ModelForm):
    ALLOWED_EMAILS = {
        "vrsec.ac.in", "iiti.ac.in", "pesu.pes.edu", "vnrvjiet.in"  # Add more institutional domains
    }
    TEAM_EMAILS = {
        "dnandinich@gmail.com", "mishajain1110@gmail.com", "praneethakalbhavi@gmail.com", "sirivoore249@gmail.com"
    }
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        max_length=32,
        label = 'First Name'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        max_length=32,
        label='Last Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        max_length=64,
        label='Email'
    )
    def clean_email(self):
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]

        if domain not in self.ALLOWED_EMAILS and email not in self.TEAM_EMAILS:
            raise ValidationError("Only institutional or team member emails are allowed.")

        return email
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
