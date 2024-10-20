from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# Users Table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')

    # Relationships
    watchlists = db.relationship('Watchlist', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    favorite_genres = db.relationship('Genre', secondary='user_genres', backref='users')

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


# Movies Table
class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.Integer)
    director = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    rating_average = db.Column(db.Float)  # New field for average rating

    # Relationships
    watchlists = db.relationship('Watchlist', backref='movie', lazy=True)
    ratings = db.relationship('Rating', backref='movie', lazy=True)
    genres = db.relationship('Genre', secondary='movie_genres', back_populates='movies')

    def __repr__(self):
        return f"<Movie(title='{self.title}', director='{self.director}', year={self.release_year})>"


# Watchlists Table
class Watchlist(db.Model):
    __tablename__ = 'watchlists'
    watchlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)

    # Modified Enum with 'dropped' status
    status = db.Column(db.Enum('watched', 'watching', 'plan_to_watch', 'dropped'), default='plan_to_watch')
    added_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Watchlist(user_id={self.user_id}, movie_id={self.movie_id}, status='{self.status}')>"


# Genres Table
class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre_name = db.Column(db.String(50), nullable=False, unique=True)

    movies = db.relationship('Movie', secondary='movie_genres', back_populates='genres')

    def __repr__(self):
        return f"<Genre(name='{self.genre_name}')>"


# Association Table for Many-to-Many Relationship between Movies and Genres
class MovieGenre(db.Model):
    __tablename__ = 'movie_genres'
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), primary_key=True)

    def __repr__(self):
        return f"<MovieGenre(movie_id={self.movie_id}, genre_id={self.genre_id})>"


# Ratings Table
class Rating(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    rated_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Rating(user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating}, review='{self.review}')>"


# New Association Table for Many-to-Many Relationship between Users and Genres
class UserGenre(db.Model):
    __tablename__ = 'user_genres'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), primary_key=True)

    def __repr__(self):
        return f"<UserGenre(user_id={self.user_id}, genre_id={self.genre_id})>"
