import functools

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        dob = request.form['dob']
        occupation = request.form['occupation']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        if not first_name:
            error = 'firstname is required.'
        elif not last_name:
            error = 'Last Name is required.'
        elif not dob:
            error = 'Date of birth is required.'
        elif not occupation:
            error = 'occupation is required.'
        elif not email:
            error = 'email is required.'
        elif not password:
            error = 'password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user(fname, lname, dob,occupation, email, password) VALUES (?,?,?,?,?,?)",
                    (first_name, last_name, dob, occupation,
                     email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"{email} is already registerd."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM WHERE email = ?", (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Email ID'
        elif not check_password_hash(user['password'], password):
            error = 'Entered incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM WHERE id = ?", (user_id,)
        ).fetchone()


@bp.route('/logout')
def log_out_user():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
