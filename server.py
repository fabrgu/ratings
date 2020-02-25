"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users. """

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    """Show user registration form or create user if email not in use."""

    if request.method == 'POST':
        email = request.form.get('email')
        user_confirmed = User.query.filter(User.email == email).all()
        if len(user_confirmed) == 0:
            user = User(email=email, password=request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash('User successfully created')
        else:
            flash('User not created. Email associated with another user.')
        return redirect('/')

    return render_template('registration.html')


@app.route('/show_login')
def show_login():
    """Show login form."""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login():
    """Logs in existing user."""

    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter(User.email == email,
                                      User.password == password).all()
    if len(existing_user) > 0:
        session['user_id'] = existing_user[0].user_id
        flash('Logged in')
        return redirect('/')
    else:
        flash('User does not exist. Please create an account.')
        return redirect('/registration')


@app.route('/logout')
def logout():
    """ log user out of session"""

    flash('You are logged out.')

    if session.get('user_id'):
        del session['user_id']
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
