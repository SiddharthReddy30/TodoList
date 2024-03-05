from flask import (
    Blueprint, render, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flask.db import get_db

bp = Blueprint('todos', __name__)


@bp.route('/index', methods=('GET', 'POST', 'UPDATE'))
def index():
    if request.method == 'GET':
        if g.user is None:
            return render_template('index.html')

        db = get_db()
        todos = db.execute(
            'SELECT t.body, status FROM todo t JOIN user u ON t.user_id = u.id'
        ).fetchall()
        return redirect(url_for('todos/todos.html', todos=todos))

    if request.method == 'POST':
         GF
