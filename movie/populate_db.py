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
        username = fake.user_name()
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            user = User(
                username=username,
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
        'https://imgs.search.brave.com/IZeE2bFct2ZtgodqFtgLwWoZg9o8HSesk3MHpMGMyP4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tb3Zp/ZXMudW5pdmVyc2Fs/cGljdHVyZXMuY29t/L21lZGlhL29wci10/c3Ixc2hlZXQzLWxv/b2syLXJnYi0zLTEt/MS02NDU0NWMwZDE1/ZjFlLTEuanBn',
        'https://imgs.search.brave.com/PhPnBQrLFT_2K2BP5p9LQt0xH78w07RA_0BBPGA8A74/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMxLnNyY2RuLmNv/bS93b3JkcHJlc3Mv/d3AtY29udGVudC91/cGxvYWRzLzIwMjQv/MDEvZHVuZS1wYXJ0/LTItcG9zdGVyLXNo/b3dpbmctdGltb3Ro/ZWUtY2hhbGFtZXQt/YXMtcGF1bC1hdHJl/aWRlcy1hbmQtemVu/ZGF5YS1hcy1jaGFu/aS1ob2xkaW5nLWRh/Z2dlcnMuanBlZw',
        'https://imgs.search.brave.com/X6Zh9zCyGnLfWWM5hcxXNepCpeeiDyyadCJCEN-O1mE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/Y29taW5nc29vbi5u/ZXQvd3AtY29udGVu/dC91cGxvYWRzL3Np/dGVzLzMvZ2FsbGVy/eS90aGUtYmF0bWFu/L3RoZS1iYXRtYW4t/cG9zdGVyLTMuanBn',
        'https://imgs.search.brave.com/oUmhi6WZnNvJEKyUD3a63iYTWwDx54w5xyM6sjFjKck/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnJl/ZGQuaXQvdXhyMnE5/YmpqOWo5MS5qcGc',
        'https://imgs.search.brave.com/CxTS-_oQI2t6b6NPwTuzYUdhdXs33tILigh7RrqklAQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9maWxt/YXJ0Z2FsbGVyeS5j/b20vY2RuL3Nob3Av/cHJvZHVjdHMvVG9w/LUd1bi1NYXZlcmlj/ay1WaW50YWdlLU1v/dmllLVBvc3Rlci1P/cmlnaW5hbC0xLVNo/ZWV0LTI3eDQxLmpw/Zz92PTE2NzA1NjIx/MDAmd2lkdGg9MTIw/MA',
        'https://imgs.search.brave.com/8qFBluDoXaH0hXif1Tx6kCgbeXnB8KcX4TlS4BETVKQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMuaW5kaWFuZXhw/cmVzcy5jb20vMjAy/My8wNS8yMDE4LW1v/dmllLXBvc3Rlci5q/cGc_dz02NDA',
        'https://imgs.search.brave.com/5vEfbmiLe40Ou1u2F_T1z6ImBR6dS3DveZ6xk0IZ7Ss/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vbW92aWVn/YWxsZXJpLm5ldC93/cC1jb250ZW50L3Vw/bG9hZHMvMjAyMi8w/OC9SYWppbmlrYW50/aC1KYWlsZXItTW92/aWUtRmlyc3QtTG9v/ay1Qb3N0ZXItSEQu/anBnP3Jlc2l6ZT02/OTYsMTA4NyZzc2w9/MQ',
        'https://imgs.search.brave.com/ZD7Uudz2pa29r10vAP2pIW8E9RLAEUujrgxk2nxMmP8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly91cGxv/YWQud2lraW1lZGlh/Lm9yZy93aWtpcGVk/aWEvZW4vdGh1bWIv/Yi9iZi9NaW5uYWxf/TXVyYWxpLmpwZy8y/MjBweC1NaW5uYWxf/TXVyYWxpLmpwZw',
        'https://imgs.search.brave.com/oOu-pJgqZJa4HrIr2-EESh3kx4llwfUGTU6Zu2K80Fc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/a2VyYWxhOS5jb20v/d3AtY29udGVudC91/cGxvYWRzLzIwMjEv/MTAva3VydXAtbW92/aWUtcG9zdGVyLTgz/OXgxMDI0LmpwZw',
        'https://imgs.search.brave.com/rHrnb26AUmNPhvXV-QqpW55hsbcXtEpdYk7pap8kEuc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93YWxs/cGFwZXJidXp6Lm5l/dC93cC1jb250ZW50/L3VwbG9hZHMvMjAy/My8wMy9qYXdhbi1w/b3N0ZXItMS5qcGc',
        'https://imgs.search.brave.com/JiHA81wIQ7eEQ_pUnCozOMbodbHF7F-LGPYGaWDBxRU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly91cGxv/YWQud2lraW1lZGlh/Lm9yZy93aWtpcGVk/aWEvZW4vYy9jMy9Q/YXRoYWFuX2ZpbG1f/cG9zdGVyLmpwZw',
    ]

    # Movie data for Hollywood, Mollywood, and Bollywood
    movie_list = [
        {"title": "Oppenheimer", "director": "Christopher Nolan", "release_year": 2023, "duration": 180,
         "description": "The story of J. Robert Oppenheimer and the creation of the atomic bomb.",
         "image_url": sample_images[0],"trailer_url":"https://youtu.be/embed/rAJ8VPXKxzInxT-y"},

        {"title": "Dune: Part Two", "director": "Denis Villeneuve", "release_year": 2024, "duration": 155,
         "description": "The continuation of Paul Atreides' journey to protect his people.",
         "image_url": sample_images[1],"trailer_url":"https://youtu.be/embed/Way9Dexny3w"},

        {"title": "The Batman", "director": "Matt Reeves", "release_year": 2022, "duration": 176,
         "description": "Batman uncovers corruption in Gotham City that connects to his own family.",
         "image_url": sample_images[2],"trailer_url":"https://youtu.be/embed/mqqft2x_Aa4"},

        {"title": "Spider-Man: No Way Home", "director": "Jon Watts", "release_year": 2021, "duration": 148,
         "description": "Peter Parker seeks help from Doctor Strange to restore his secret identity.",
         "image_url": sample_images[3],"trailer_url":"https://youtu.be/embed/JfVOs4VSpmA"},

        {"title": "Top Gun: Maverick", "director": "Joseph Kosinski", "release_year": 2022, "duration": 130,
         "description": "Maverick returns to train a new squad of Top Gun graduates.", "image_url": sample_images[4],
         "trailer_url":"https://youtu.be/embed/giXco2jaZ_4"},

        {"title": "2018", "director": "Jude Anthony Joseph", "release_year": 2023, "duration": 150,
         "description": "A film about the Kerala floods.", "image_url": sample_images[5],
         "trailer_url":"https://youtu.be/embed/Af3cjNPhM4o"},

        {"title": "Jailer", "director": "Nelson Dilipkumar", "release_year": 2023, "duration": 168,
         "description": "A retired cop faces a criminal kingpin.", "image_url": sample_images[6],
         "trailer_url": "https://youtu.be/embed/Y5BeWdODPqo"},

        {"title": "Minnal Murali", "director": "Basil Joseph", "release_year": 2021, "duration": 158,
         "description": "An ordinary man gains superpowers.", "image_url": sample_images[7],
         "trailer_url": "https://youtu.be/embed/zAUAliz1TKA"},

        {"title": "Kurup", "director": "Srinath Rajendran", "release_year": 2021, "duration": 155,
         "description": "A story of the fugitive Sukumara Kurup.", "image_url": sample_images[8],
         "trailer_url": "https://youtu.be/embed/L13AUL0HkDk"},

        {"title": "Jawan", "director": "Atlee", "release_year": 2023, "duration": 169,
         "description": "A man confronts his enemies from the past.", "image_url": sample_images[9],
         "trailer_url": "https://youtu.be/embed/MWOlnZSnXJo"},

        {"title": "Pathaan", "director": "Siddharth Anand", "release_year": 2023, "duration": 146,
         "description": "An Indian spy stops an attack on his homeland.", "image_url": sample_images[10],
         "trailer_url": "https://youtu.be/embed/vqu4z34wENw"},
    ]

    for movie_data in movie_list:
        # Check if the movie already exists
        existing_movie = Movie.query.filter_by(title=movie_data["title"]).first()
        if existing_movie is None:  # If it does not exist, create it
            movie = Movie(
                title=movie_data["title"],
                director=movie_data["director"],
                release_year=movie_data["release_year"],
                duration=movie_data["duration"],
                description=movie_data["description"],
                image_url=movie_data["image_url"],
                trailer_url=movie_data["trailer_url"]
            )
            db.session.add(movie)

    db.session.commit()


def create_genres():
    genre_list = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi']

    for genre_name in genre_list:
        existing_genre = Genre.query.filter_by(genre_name=genre_name).first()
        if existing_genre is None:
            genre = Genre(genre_name=genre_name)
            db.session.add(genre)
    db.session.commit()



def create_movie_genres():
    movies = Movie.query.all()
    genres = Genre.query.all()

    for movie in movies:
        chosen_genres = choice(genres)
        if chosen_genres not in movie.genres:
            movie.genres.append(chosen_genres)

    db.session.commit()


def create_watchlists():
    user_ids = [user.user_id for user in User.query.all()]
    movie_ids = [movie.movie_id for movie in Movie.query.all()]
    status_options = ['watching', 'plan_to_watch', 'watched']

    for _ in range(5):
        user_id = choice(user_ids)
        movie_id = choice(movie_ids)
        existing_watchlist = Watchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing_watchlist is None:
            watchlist = Watchlist(
                user_id=user_id,
                movie_id=movie_id,
                status=choice(status_options),
                added_at=fake.date_time_this_year()
            )
            db.session.add(watchlist)
    db.session.commit()

def create_ratings():
    user_ids = [user.user_id for user in User.query.all()]
    movie_ids = [movie.movie_id for movie in Movie.query.all()]

    for _ in range(5):
        user_id = choice(user_ids)
        movie_id = choice(movie_ids)
        existing_rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing_rating is None:
            rating = Rating(
                user_id=user_id,
                movie_id=movie_id,
                rating=randint(1, 10),
                review=fake.text(),
                rated_at=fake.date_time_this_year()
            )
            db.session.add(rating)
    db.session.commit()

def get_embedded_url(trailer_url):
    if 'youtube.com/watch?v=' in trailer_url:
        video_id = trailer_url.split('v=')[1]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtu.be/' in trailer_url:
        video_id = trailer_url.split('/')[-1]
        return f'https://www.youtube.com/watch?v={video_id}'
    return trailer_url


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
