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
    movies = Movie.query.all()
    return render_template('home.html', posts=movies)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register",methods=['GET', 'POST'])
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
    return render_template('register.html',title='Register',form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html',users=users)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie, 'Watchlist': Watchlist, 'Genre': Genre, 'Rating': Rating, 'MovieGenre': MovieGenre}

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

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn



@app.route("/account",  methods=['GET', 'POST'])
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
    image_file = url_for('static', filename='pic/'+current_user.image_file)
    return render_template("account.html", title='Account',
                           image_file=image_file, form=form)

cache = Cache(app)


@app.route('/movies')
@cache.cached(timeout=60)
def movies():
    posts = Movie.query.all()
    return render_template('home.html', posts=posts)

if __name__ == '__main__':
        with app.app_context():
            db.create_all()
            print("database populated!!!!")
        app.run(debug=True)

