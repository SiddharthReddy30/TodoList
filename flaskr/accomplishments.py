from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
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
    return render_template('accomplshiments/index.html', accomps= accomps)
