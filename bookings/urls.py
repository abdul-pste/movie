"""
Author: Abdullahi Nur
BU Email: anur@bu.edu
Description: This file defines URL patterns for the Movie Booking application. 
             Each pattern maps a specific URL path to its corresponding view.
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home and movie-related URLs
    path('', views.movie_list, name='home'),  # Home page displaying movie list
    path('movies/', views.movie_list, name='movie_list'),  # List of all movies
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),  # Movie details
    path('movies/<int:movie_id>/add_showtime/', views.add_showtime, name='add_showtime'),  # Add showtime to a movie

    # Booking-related URLs
    path('book/<int:showtime_id>/', views.book_showtime, name='book_showtime'),  # Book tickets for a showtime
    path('booking/history/', views.booking_history, name='booking_history'),  # View booking history
    path('delete/history/', views.delete_all_bookings, name='delete_history'),  # Delete all bookings

    # User profile and authentication URLs
    path('profile/', views.profile, name='profile'),  # View user profile
    path('edit/profile/', views.edit_profile, name='edit_profile'),  # Edit user profile
    path('logout/', views.logout, name='logout'),  # User logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # User login
    path('register/', views.register, name='register'),  # User registration
]
