"""
This file defines the URL routing for the Movie Booking application.

Routes:
- `/`: Home page displaying the movie list (view: `movie_list`).
- `/movies/`: Lists all available movies (view: `movie_list`).
- `/movies/<int:movie_id>/`: Displays details of a specific movie (view: `movie_detail`).
- `/booking/history/`: Displays the booking history for the logged-in user (view: `booking_history`).
- `/delete/history/`: Clears all bookings for the logged-in user (view: `delete_all_bookings`).
- `/profile/`: Displays the profile page for the logged-in user (view: `profile`).
- `/edit/profile/`: Allows users to edit their profile (view: `edit_profile`).
- `/logout/`: Logs out the user (view: `logout`).
- `/login/`: Displays the login page (Django's `LoginView`).
- `/register/`: Displays the registration page (view: `register`).
- `/book/<int:showtime_id>/`: Handles booking a specific showtime (view: `book_showtime`).
- `/movies/<int:movie_id>/add_showtime/`: Allows adding a new showtime for a movie (view: `add_showtime`).

These routes map user requests to the corresponding views, enabling seamless navigation within the application.
"""


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.movie_list, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    #path('book/<int:showtime_id>/', views.book_showtime, name='book_showtime'),
    path('booking/history/', views.booking_history, name='booking_history'),
    path('delete/history/', views.delete_all_bookings, name='delete_history'),
    path('profile/', views.profile, name='profile'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('book/<int:showtime_id>/', views.book_showtime, name='book_showtime'),
    path('movies/<int:movie_id>/add_showtime/', views.add_showtime, name='add_showtime'),
]
