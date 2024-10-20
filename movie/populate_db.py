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


def reset_movies():
    # Step 1: Delete all existing movies
    delete_all_movies()

    # Step 2: Insert new movies
    create_movies()


def delete_all_movies():
    movies = Movie.query.all()  # Query all existing movie records
    for movie in movies:
        db.session.delete(movie)  # Delete each movie
    db.session.commit()  # Commit the changes to the database


def create_movies():
    sample_images = [
        'https://via.placeholder.com/150',  # Placeholder image
        'https://via.placeholder.com/150/FF0000/FFFFFF?text=Action',
        'https://via.placeholder.com/150/00FF00/FFFFFF?text=Comedy',
        'https://via.placeholder.com/150/0000FF/FFFFFF?text=Drama',
        'https://via.placeholder.com/150/FFFF00/FFFFFF?text=Horror',
        'https://via.placeholder.com/150/FF00FF/FFFFFF?text=Sci-Fi',
    ]

    # Movie data for Hollywood, Mollywood, and Bollywood
    movie_list = [
        {"title": "Oppenheimer", "director": "Christopher Nolan", "release_year": 2023, "duration": 180,
         "description": "The story of J. Robert Oppenheimer and the creation of the atomic bomb.",
         "image_url": sample_images[0]},
        {"title": "Dune: Part Two", "director": "Denis Villeneuve", "release_year": 2024, "duration": 155,
         "description": "The continuation of Paul Atreides' journey to protect his people.",
         "image_url": sample_images[1]},
        {"title": "The Batman", "director": "Matt Reeves", "release_year": 2022, "duration": 176,
         "description": "Batman uncovers corruption in Gotham City that connects to his own family.",
         "image_url": sample_images[2]},
        {"title": "Spider-Man: No Way Home", "director": "Jon Watts", "release_year": 2021, "duration": 148,
         "description": "Peter Parker seeks help from Doctor Strange to restore his secret identity.",
         "image_url": sample_images[3]},
        {"title": "Top Gun: Maverick", "director": "Joseph Kosinski", "release_year": 2022, "duration": 130,
         "description": "Maverick returns to train a new squad of Top Gun graduates.", "image_url": sample_images[4]},
        {"title": "2018", "director": "Jude Anthany Joseph", "release_year": 2023, "duration": 150,
         "description": "A film about the Kerala floods.", "image_url": sample_images[5]},
        {"title": "Jailer", "director": "Nelson Dilipkumar", "release_year": 2023, "duration": 168,
         "description": "A retired cop faces a criminal kingpin.", "image_url": sample_images[1]},
        {"title": "Minnal Murali", "director": "Basil Joseph", "release_year": 2021, "duration": 158,
         "description": "An ordinary man gains superpowers.", "image_url": sample_images[2]},
        {"title": "Kurup", "director": "Srinath Rajendran", "release_year": 2021, "duration": 155,
         "description": "A story of the fugitive Sukumara Kurup.", "image_url": sample_images[4]},
        {"title": "Jawan", "director": "Atlee", "release_year": 2023, "duration": 169,
         "description": "A man confronts his enemies from the past.", "image_url": sample_images[5]},
        {"title": "Pathaan", "director": "Siddharth Anand", "release_year": 2023, "duration": 146,
         "description": "An Indian spy stops an attack on his homeland.", "image_url": sample_images[0]},
    ]

    for movie_data in movie_list:
        movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            release_year=movie_data["release_year"],
            duration=movie_data["duration"],
            description=movie_data["description"],
            image_url=movie_data["image_url"]
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
