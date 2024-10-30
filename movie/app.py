import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from db_models import db, User, Movie, Watchlist, Genre, Rating, MovieGenre
from forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_migrate import Migrate, upgrade
from flask_caching import Cache

app = Flask(__name__)
app.config["SECRET_KEY"] = '0b89eaaafda4d7eb310aab385265275c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  # Get the current page number from query parameters, default to 1
    per_page = 6  # Set the number of movies to display per page
    movies = Movie.query.paginate(page, per_page, error_out=False)  # Paginate the movie query

    return render_template('home.html', posts=movies.items, current_page=movies.page, total_pages=movies.pages)  # Render home.html with movie data

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie, 'Watchlist': Watchlist, 'Genre': Genre, 'Rating': Rating,
            'MovieGenre': MovieGenre}


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        #            flash('Logged in', 'success')
        else:
            flash('Invalid Credentials! Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pic', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pic/' + current_user.image_file)
    return render_template("account.html", title='Account',
                           image_file=image_file, form=form)


cache = Cache(app)


@app.route('/movies')
@cache.cached(timeout=60)
def movies():
    posts = Movie.query.all()
    return render_template('home.html', posts=posts)


@app.route('/add_to_watchlist/<int:movie_id>', methods=['POST'])
@login_required
def add_to_watchlist(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash("Movie not found.", "danger")
        return redirect(url_for('home'))

    # Check if the movie is already in the user's watchlist
    watchlist_entry = Watchlist.query.filter_by(user_id=current_user.user_id, movie_id=movie_id).first()

    if not watchlist_entry:
        new_entry = Watchlist(user_id=current_user.user_id, movie_id=movie_id)
        db.session.add(new_entry)
        db.session.commit()
        flash("Movie added to watchlist!", "success")
    else:
        flash("Movie is already in your watchlist.", "info")

    return redirect(url_for('movie_detail', movie_id=movie_id))


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    genres = ', '.join([genre.genre_name for genre in movie.genres])
    reviews = Rating.query.filter_by(movie_id=movie_id).all()

    # Check if the movie is already in the user's watchlist
    in_watchlist = False
    if current_user.is_authenticated:
        in_watchlist = Watchlist.query.filter_by(user_id=current_user.user_id, movie_id=movie_id).first() is not None

    return render_template('movie_detail.html', movie=movie, genres=genres, reviews=reviews, in_watchlist=in_watchlist)


@app.route('/watchlist')
@login_required
def watchlist():
    print("Watchlist route accessed")  # Debugging output
    # Fetch the watchlist entries for the current user
    watchlist_entries = Watchlist.query.filter_by(user_id=current_user.user_id).all()

    # Retrieve the corresponding movies from the Movie model
    movies = [Movie.query.get(entry.movie_id) for entry in watchlist_entries]

    return render_template('watchlist.html', movies=movies)


@app.route('/remove_from_watchlist/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_watchlist(movie_id):
    watchlist_entry = Watchlist.query.filter_by(user_id=current_user.user_id, movie_id=movie_id).first()
    if watchlist_entry:
        db.session.delete(watchlist_entry)
        db.session.commit()
        flash("Movie removed from watchlist!", "success")
    else:
        flash("Movie not found in your watchlist.", "info")

    return redirect(url_for('watchlist'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("database populated!!!!")
    app.run(debug=True)
