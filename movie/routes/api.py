import api
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..db_models import Movie, Watchlist


@api.route('/watchlist')
@login_required
def watchlist():
    # Query the user's watchlist
    watchlist_movies = Watchlist.query.filter_by(user_id=current_user.user_id).all()

    # Fetch movie details for the watchlist
    movies = [movie for movie in watchlist_movies]

    return render_template('watchlist.html', movies=movies)
