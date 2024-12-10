from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
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
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Field used for authentication
    REQUIRED_FIELDS = ['name']  # Fields required when creating a user

    def __str__(self):
        return self.email

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)  # Ensure this field exists

    def get_poster_url(self):
        poster_urls = {
    "Eternals": "https://path-to-eternals-poster.jpg",
    "Dune": "https://path-to-dune-poster.jpg",
    "The Shawshank Redemption": "https://www.themoviedb.org/t/p/original/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
    "The Dark Knight": "https://www.themoviedb.org/t/p/original/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg",
    "Inception": "https://www.themoviedb.org/t/p/original/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    "Forrest Gump": "https://www.themoviedb.org/t/p/original/saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
    "The Matrix": "https://www.themoviedb.org/t/p/original/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "Pulp Fiction": "https://www.themoviedb.org/t/p/original/dM2w364MScsjFf8pfMbaWUcWrR.jpg",
    "The Godfather": "https://www.themoviedb.org/t/p/original/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "The Lion King": "https://www.themoviedb.org/t/p/original/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg",
    "Interstellar": "https://www.themoviedb.org/t/p/original/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
    "Gladiator": "https://www.themoviedb.org/t/p/original/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg",
    "Avengers: Endgame": "https://www.themoviedb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
    "The Silence of the Lambs": "https://www.themoviedb.org/t/p/original/ruXHUA3KiiLEjCwvSqKuxe9OAH8.jpg",
    "Joker": "https://www.themoviedb.org/t/p/original/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
    "Whiplash": "https://www.themoviedb.org/t/p/original/tcTDZk0PZq6oWhGHmTOfQH81GnI.jpg",
    "Parasite": "https://www.themoviedb.org/t/p/original/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "The Grand Budapest Hotel": "https://www.themoviedb.org/t/p/original/nX5XotM9yprCKarRH4fzOq1VM1J.jpg",
    "Shutter Island": "https://www.themoviedb.org/t/p/original/52d7CAc3yr3SyWdjLWiWEf74EQc.jpg",
    "The Social Network": "https://www.themoviedb.org/t/p/original/m03jul0YdVEOFXEQVUv6pOVQYGL.jpg",
    "The Wolf of Wall Street": "https://www.themoviedb.org/t/p/original/vK1o5rZGqxyovfIhZyMELhk03wO.jpg",
    "La La Land": "https://www.themoviedb.org/t/p/original/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
}

        return poster_urls.get(self.title, "https://via.placeholder.com/150")

    def __str__(self):
        return self.title


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    cinema_hall = models.CharField(max_length=255)  # New field for cinema hall
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
