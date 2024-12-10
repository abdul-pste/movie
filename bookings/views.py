"""
Author: Abdullahi Nur
BU Email: anur@bu.edu
Description: This file contains the view functions for the Movie Booking application, 
             handling user interaction, API integration, and data processing.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import Movie, Showtime, Booking
from .forms import BookingForm, LoginForm, CustomUserCreationForm, ShowtimeForm


def home(request):
    """
    Render the homepage with a form to search for movies. 
    If a POST request is received, fetch and save movie data.
    """
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['q']
            location = form.cleaned_data['location']

            # Fetch data from API
            params = {
                "q": query,
                "location": location,
                "hl": "en",
                "gl": "us",
                "api_key": "YOUR_SERPAPI_KEY"
            }
            search = GoogleSearch(params)
            result = search.get_dict()

            # Debugging: Check the API response
            print(result)

            # Process the API response
            if "showtimes" in result:
                for showtime_data in result['showtimes']:
                    movie_title = query.lower()
                    movie, created = Movie.objects.get_or_create(
                        title=movie_title,
                        defaults={'poster_url': showtime_data.get('poster_url', 'https://via.placeholder.com/150')}
                    )
                    if not created and not movie.poster_url:
                        movie.poster_url = showtime_data.get('poster_url', 'https://via.placeholder.com/150')
                        movie.save()

                    Showtime.objects.create(
                        movie=movie,
                        date=showtime_data.get('date', 'N/A'),
                        time=showtime_data.get('time', 'N/A'),
                        cinema_hall=showtime_data.get('cinema_hall', 'N/A')
                    )
            return redirect('movie_list')
    else:
        form = MovieSearchForm()

    return render(request, 'home.html', {'form': form})


def movie_list(request):
    """
    Display a list of movies with showtimes.
    """
    movies = Movie.objects.prefetch_related('showtimes').all()
    return render(request, 'movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    """
    Display details for a specific movie, including showtimes.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    return render(request, 'movie_detail.html', {'movie': movie, 'showtimes': showtimes})


@login_required
def add_showtime(request, movie_id):
    """
    Add a new showtime to a specific movie.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ShowtimeForm(request.POST)
        if form.is_valid():
            showtime = form.save(commit=False)
            showtime.movie = movie
            showtime.save()
            return redirect('movie_list')
    else:
        form = ShowtimeForm()

    return render(request, 'book_showtime.html', {'form': form, 'movie': movie, 'form_mode': 'add'})


@login_required
def book_showtime(request, showtime_id):
    """
    Allow a user to book tickets for a specific showtime.
    """
    showtime = get_object_or_404(Showtime, id=showtime_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.showtime = showtime
            booking.total_cost = booking.tickets * 10.00
            booking.save()
            return redirect('booking_history')
    else:
        form = BookingForm()

    return render(request, 'book_showtime.html', {'form': form, 'showtime': showtime, 'form_mode': 'book'})


def booking_history(request):
    """
    Display a user's booking history.
    """
    bookings = Booking.objects.filter(user=request.user).select_related("showtime", "showtime__movie")
    return render(request, "booking_history.html", {"bookings": bookings})


def delete_all_bookings(request):
    """
    Delete all bookings for the logged-in user.
    """
    if request.method == "POST" and request.user.is_authenticated:
        Booking.objects.filter(user=request.user).delete()
        return redirect('booking_history')
    return redirect('login')


@login_required
def profile(request):
    """
    Render the user's profile page.
    """
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    """
    Allow a user to edit their profile information.
    """
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def custom_login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    """
    Handle user logout.
    """
    auth_logout(request)
    return redirect('home')


def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
