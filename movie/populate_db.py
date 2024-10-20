from faker import Faker
from sqlalchemy.exc import IntegrityError
from random import randint, choice
from werkzeug.security import generate_password_hash
from db_models import db, User, Watchlist, Rating, Movie, Genre, MovieGenre
from app import app

fake = Faker()

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
    sample_images = [
        'https://via.placeholder.com/150',  # Placeholder image
        'https://via.placeholder.com/150/FF0000/FFFFFF?text=Action',
        'https://via.placeholder.com/150/00FF00/FFFFFF?text=Comedy',
        'https://via.placeholder.com/150/0000FF/FFFFFF?text=Drama',
        'https://via.placeholder.com/150/FFFF00/FFFFFF?text=Horror',
        'https://via.placeholder.com/150/FF00FF/FFFFFF?text=Sci-Fi',
    ]

    for _ in range(5):
        movie = Movie(
            title=fake.sentence(nb_words=3),
            director=fake.name(),
            release_year=fake.year(),
            duration=randint(90, 180),  # Duration in minutes
            description=fake.text(),
            image_url=choice(sample_images)  # Choose a random image from the sample list
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
    movies = Movie.query.all()
    genres = Genre.query.all()

    for movie in movies:
        chosen_genres = choice(genres)
        movie.genres.append(chosen_genres)

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
        db.create_all()
        create_users()
        create_movies()
        create_genres()
        create_movie_genres()
        create_watchlists()
        create_ratings()

    print("Database populated successfully!")
