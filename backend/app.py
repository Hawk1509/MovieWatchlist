from flask import Flask,render_template, url_for, flash, redirect
from db_models import  db,User, Movie, Watchlist, Genre, Rating, MovieGenre
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = '0b89eaaafda4d7eb310aab385265275c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app)

posts = [
    {
      "year": 2023,
      "title": "Oppenheimer",
      "director": "Christopher Nolan",
      "review": "A gripping historical drama that explores the life of J. Robert Oppenheimer and the development of the atomic bomb.",
      "runtime": 180
    },
    {
      "year": 2023,
      "title": "Barbie",
      "director": "Greta Gerwig",
      "review": "A fun and imaginative take on the iconic doll, filled with vibrant visuals and a humorous narrative.",
      "runtime": 114
    },
    {
      "year": 2022,
      "title": "Everything Everywhere All at Once",
      "director": "Daniel Kwan, Daniel Scheinert",
      "review": "A mind-bending sci-fi adventure that weaves together multiple universes in a touching family story.",
      "runtime": 139
    },
    {
      "year": 2022,
      "title": "Top Gun: Maverick",
      "director": "Joseph Kosinski",
      "review": "A high-octane sequel that delivers stunning aerial sequences and a nostalgic return to the skies.",
      "runtime": 131
    },
    {
      "year": 2021,
      "title": "Dune",
      "director": "Denis Villeneuve",
      "review": "An epic adaptation of Frank Herbert's novel, showcasing breathtaking visuals and a captivating storyline.",
      "runtime": 155
    },
    {
      "year": 2021,
      "title": "Spider-Man: No Way Home",
      "director": "Jon Watts",
      "review": "A thrilling entry into the Spider-Man franchise that brings together beloved characters from different universes.",
      "runtime": 148
    },
    {
      "year": 2020,
      "title": "Nomadland",
      "director": "Chloé Zhao",
      "review": "A poignant portrayal of modern-day nomadic life, beautifully captured through Frances McDormand's performance.",
      "runtime": 107
    },
    {
      "year": 2020,
      "title": "Soul",
      "director": "Pete Docter, Kemp Powers",
      "review": "A heartwarming animated film that explores the meaning of life and passion through jazz music.",
      "runtime": 100
    },
    {
      "year": 2019,
      "title": "Parasite",
      "director": "Bong Joon-ho",
      "review": "A darkly comedic thriller that tackles class disparity, winning the Academy Award for Best Picture.",
      "runtime": 132
    },
    {
      "year": 2019,
      "title": "1917",
      "director": "Sam Mendes",
      "review": "A visually stunning war film that immerses viewers in the harrowing experience of a soldier's mission during WWI.",
      "runtime": 119
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html',users=users)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie, 'Watchlist': Watchlist, 'Genre': Genre, 'Rating': Rating, 'MovieGenre': MovieGenre}


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@movies.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Credentials! Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
        with app.app_context():
            db.create_all()
            print("database populated!!!!")
        app.run(debug=True)

