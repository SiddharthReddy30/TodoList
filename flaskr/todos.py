from flask import (
    Blueprint, render, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flask.db import get_db

bp = Blueprint('todos', __name__)


@bp.route('/index')
def index():
    if g.user is None:
        return render_template('todos/index.html')
    return redirect(url_for(todos.todos))


@bp.route('/todos', methods=('GET', 'POST', 'UPDATE'))
@login_required
def todos():
    if request.method == 'GET':

        db = get_db()

        todos = db.execute(
            'SELECT t.body, status FROM todo t JOIN user u ON t.user_id = u.id'
        ).fetchall()
        return render_template('todos/todos.html', todos=todos)
