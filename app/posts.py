import datetime

from flask import (
    Blueprint, session, flash, render_template, request
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

now = datetime.datetime.now()
current_year = now.year
bp = Blueprint('posts', __name__)


@bp.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    db = get_db()
    posts = db.execute(
        'SELECT p.id, body, created'
        ' FROM post p JOIN user u ON p.dest = u.id'
        ' WHERE u.id = {}'
        ' ORDER BY created DESC'.format(user_id)
    ).fetchall()
    return render_template('posts/index.html', posts=posts, year=current_year)


@bp.route('/<string:username>/send', methods=('GET', 'POST'))
def create(username):
    db = get_db()
    if request.method == 'POST':
        body = request.form['body']
        dest = db.execute(
            'SELECT id from user where username= ?', (username,)
        ).fetchone()['id']
        error = None

        if dest is None:
            error = 'User doesn\'t exist'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (body, dest)'
                ' VALUES (?, ?)',
                (body, dest)
            )
            db.commit()
            return render_template('posts/sent.html', user=username)

    if request.method == 'GET':
        dest = db.execute(
            'SELECT id from user where username= ?', (username,)
        ).fetchone()
        if dest is None:
            abort(404)
        else:
            return render_template('posts/create.html', user=username)


@bp.route('/sendsomeone')
def send():
    return render_template('send_a_message.html')
