from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exception import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('accomplishments', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    accomps = db.execute(
        ' SELECT t.id,body, status, user_id'
        'FROM todo t JOIN user u ON t.user_id = u.id'
    ).fetchall()
    return render_template('accomplshiments/index.html', accomps=accomps)


def get_accomp(id):
    accomp = get_db().execute(
        ' SELECT t.id, body, status, user_id'
        ' FROM todo t user u ON t.user_id = u.id'
        ' WHERE t.id = ?'
        (id,)
    ).fetchone()

    if accomp['user_id'] != g.user['id']:
        abort(403)
    return accomp


@bp.route('/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete(todo_id):
    try:
        get_accomp(todo_id)
        db = get_db()
        db.execute('DELETE FROM todo WHERE id = ?', (todo_id,))
        db.commit()
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)


@bp.route("/create", methods=['POST'])
@login_required
def create(task_id):
    input = request.get_json()
    body = input['body']

    if not body:
        result = {'success': False, 'response': 'Task can\'t be empty'}
    else:
        db = get_db()
        db.execute(
            'INSERT INTO todo (user_id, body, status)'
            'VALUES (?, ?, ?)',
            (g.user['id'], body, 0)
        )
        db.commit()
        result = {'success': True, 'response': 'Done'}
        return jsonify(result)


