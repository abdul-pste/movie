from bookings.models import Movie

# Hardcoded dictionary of movie titles and their poster URLs
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

# Update the poster_url field for each movie
for title, url in poster_urls.items():
    movie = Movie.objects.filter(title=title).first()
    if movie:
        movie.poster_url = url
        movie.save()
        print(f"Updated {title} poster URL.")
    else:
        print(f"Movie '{title}' not found in the database.")
