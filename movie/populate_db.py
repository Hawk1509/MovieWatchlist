from faker import Faker
from sqlalchemy.exc import IntegrityError
from random import randint, choice
from werkzeug.security import generate_password_hash
from db_models import db, User, Watchlist, Rating, Movie, Genre, MovieGenre  # Import movie_genres association table
from app import app

fake = Faker()

# Password for all users
hashed_password = generate_password_hash('123')


def create_users():
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=hashed_password,
            created_at=fake.date_time_this_year()
        )
        db.session.add(user)
    db.session.commit()


def create_movies():
    for _ in range(5):
        movie = Movie(
            title=fake.sentence(nb_words=3),
            director=fake.name(),
            release_year=fake.year(),
            duration=randint(90, 180),  # Duration in minutes
            description=fake.text()
        )
        db.session.add(movie)
    db.session.commit()


def create_genres():
    genre_list = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi']
    for genre_name in genre_list:
        existing_genre = Genre.query.filter_by(genre_name=genre_name).first()
        if not existing_genre:
            genre = Genre(genre_name=genre_name)
            db.session.add(genre)
    db.session.commit()


def create_movie_genres():
    # Fetch all movies and genres from the database
    movies = Movie.query.all()
    genres = Genre.query.all()

    for movie in movies:
        # Randomly choose a number of genres to associate with the movie (e.g., between 1 and 3)
        chosen_genres = choice(genres)  # Choose a random genre
        movie.genres.append(chosen_genres)  # Append the chosen genre to the movie

    db.session.commit()  # Commit the changes


def create_watchlists():
    user_ids = [user.user_id for user in User.query.all()]
    movie_ids = [movie.movie_id for movie in Movie.query.all()]
    status_options = ['watching', 'plan_to_watch', 'watched']

    for _ in range(5):
        watchlist = Watchlist(
            user_id=choice(user_ids),
            movie_id=choice(movie_ids),
            status=choice(status_options),
            added_at=fake.date_time_this_year()
        )
        db.session.add(watchlist)
    db.session.commit()


def create_ratings():
    user_ids = [user.user_id for user in User.query.all()]
    movie_ids = [movie.movie_id for movie in Movie.query.all()]

    for _ in range(5):
        rating = Rating(
            user_id=choice(user_ids),
            movie_id=choice(movie_ids),
            rating=randint(1, 10),
            review=fake.text(),
            rated_at=fake.date_time_this_year()
        )
        db.session.add(rating)
    db.session.commit()


if __name__ == "__main__":
    # Initialize the database and populate the tables
    with app.app_context():
        db.create_all()  # Make sure all tables are created
        create_users()
        create_movies()
        create_genres()
        create_movie_genres()  # Ensure this is called after create_movies and create_genres
        create_watchlists()
        create_ratings()

    print("Database populated successfully!")
