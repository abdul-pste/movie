"""
Author: Abdullahi Nur
BU Email: anur@bu.edu
Description: This file defines the models for the Movie Booking application, 
             including a custom user model, movies, showtimes, and bookings. 
             These models form the core of the database schema.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Manager for the custom User model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.

        Args:
            email (str): User's email.
            password (str): User's password.
            extra_fields (dict): Additional fields for the user.

        Returns:
            User: A new user instance.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.

        Args:
            email (str): Superuser's email.
            password (str): Superuser's password.
            extra_fields (dict): Additional fields for the user.

        Returns:
            User: A new superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the unique identifier.
    """
    email = models.EmailField(unique=True)  # Unique identifier
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Movie(models.Model):
    """
    Model to represent a movie.
    """
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)  # Duration in minutes
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)

    def get_poster_url(self):
        """
        Return the poster URL for the movie. If not available, return a placeholder URL.
        """
        poster_urls = {
            "Eternals": "https://path-to-eternals-poster.jpg",
            "Dune": "https://path-to-dune-poster.jpg",
            "The Shawshank Redemption": "https://www.themoviedb.org/t/p/original/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
            "The Dark Knight": "https://www.themoviedb.org/t/p/original/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg",
            # Add other movies here...
            "La La Land": "https://www.themoviedb.org/t/p/original/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
        }
        return poster_urls.get(self.title, "https://via.placeholder.com/150")

    def __str__(self):
        return self.title


class Showtime(models.Model):
    """
    Model to represent a showtime for a movie.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    cinema_hall = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Showtime for {self.movie.title} at {self.cinema_hall}"


class Booking(models.Model):
    """
    Model to represent a user's booking for a showtime.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    tickets = models.PositiveIntegerField(default=1)  # Default to 1 if not specified
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Booking by {self.user.email} for {self.showtime}"
