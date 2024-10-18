from faker import Faker
from app import db, app, User, Movie, Watchlist, Genre, Rating, MovieGenre
import random

# Initialize Faker
fake = Faker()

# Genres for random selection
genre_names = ['Action', 'Drama', 'Comedy', 'Horror', 'Thriller', 'Sci-Fi', 'Documentary']


def create_genres():
    genres = []
    for genre_name in genre_names:
        genre = Genre(genre_name=genre_name)
        genres.append(genre)
        db.session.add(genre)
    db.session.commit()
    return genres


def create_users(num_users=10):
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        db.session.add(user)
    db.session.commit()


def create_movies(num_movies=20):
    for _ in range(num_movies):
        movie = Movie(
            title=fake.catch_phrase(),
            release_year=random.randint(1980, 2023),
            director=fake.name(),
            duration=random.randint(90, 180),
            description=fake.paragraph(nb_sentences=5)
        )
        db.session.add(movie)
    db.session.commit()


def create_watchlists():
    users = User.query.all()
    movies = Movie.query.all()

    for user in users:
        for _ in range(random.randint(1, 5)):  # Random number of watchlist entries per user
            movie = random.choice(movies)
            watchlist = Watchlist(
                user_id=user.user_id,
                movie_id=movie.movie_id,
                status=random.choice(['watched', 'watching', 'plan_to_watch'])
            )
            db.session.add(watchlist)
    db.session.commit()


def create_ratings():
    users = User.query.all()
    movies = Movie.query.all()

    for user in users:
        for _ in range(random.randint(1, 5)):  # Random number of ratings per user
            movie = random.choice(movies)
            rating = Rating(
                user_id=user.user_id,
                movie_id=movie.movie_id,
                rating=random.randint(1, 10),
                review=fake.sentence()
            )
            db.session.add(rating)
    db.session.commit()


def create_movie_genres():
    genres = Genre.query.all()
    movies = Movie.query.all()

    for movie in movies:
        selected_genres = random.sample(genres, random.randint(1, 3))  # Each movie gets 1-3 genres
        for genre in selected_genres:
            movie_genre = MovieGenre(movie_id=movie.movie_id, genre_id=genre.genre_id)
            db.session.add(movie_genre)
    db.session.commit()


def populate_db():
    db.drop_all()  # Drop all tables if needed (optional)
    db.create_all()  # Create tables
    create_genres()
    create_users()
    create_movies()
    create_watchlists()
    create_ratings()
    create_movie_genres()
    print("Database populated with random content.")


if __name__ == '__main__':
    with app.app_context():
        populate_db()
