"""
Author: Abdullahi Nur
BU Email: anur@bu.edu
Description: This file contains the forms used in the Movie Booking application. These forms 
             define user input structures for user registration, login, movie search, showtime 
             creation, and booking functionalities. The forms integrate with the Django forms 
             framework and the models defined in the project.
"""

from django import forms
from .models import User, Movie, Showtime, Booking
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    """
    Form for creating or updating a user.
    
    Fields:
        name (str): The user's name.
        email (str): The user's email.
        password (str): The user's password (masked as input).
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Render password input as a password field
        }

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user using the custom User model.

    Fields:
        email (str): User's email for login.
        password1 (str): User's password.
        password2 (str): Confirmation of the password.
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class MovieSearchForm(forms.Form):
    """
    Form for searching movies based on title and location.
    
    Fields:
        q (str): The movie title to search for.
        location (str): The location where the search should be conducted.
    """
    q = forms.CharField(label='Movie Title', max_length=100, required=True)
    location = forms.CharField(label='Location', max_length=100, required=True)

class MovieForm(forms.ModelForm):
    """
    Form for creating or updating a movie.

    Fields:
        title (str): The title of the movie.
    """
    class Meta:
        model = Movie
        fields = ['title']

class ShowtimeForm(forms.ModelForm):
    """
    Form for creating or updating a showtime.

    Fields:
        date (date): The date of the showtime.
        time (time): The time of the showtime.
        cinema_hall (str): The hall where the showtime is hosted.
    """
    class Meta:
        model = Showtime
        fields = ['date', 'time', 'cinema_hall']

class BookingForm(forms.ModelForm):
    """
    Form for creating or updating a booking.

    Fields:
        tickets (int): The number of tickets being booked.
    """
    class Meta:
        model = Booking
        fields = ["tickets"]  # Add other fields as needed
        widgets = {
            "tickets": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }

class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering a new user.

    Fields:
        name (str): The user's name.
        email (str): The user's email.
        password (str): The user's password (masked as input).
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Render password input as masked
        }

class LoginForm(forms.Form):
    """
    Form for user login.

    Fields:
        email (str): The user's email.
        password (str): The user's password (masked as input).
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
