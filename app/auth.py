import datetime
import functools
# Retrieving Gmail credentials
import secrets
import smtplib

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
from itsdangerous import URLSafeTimedSerializer
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

now = datetime.datetime.now()
current_year = now.year

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/recover', methods=('GET', 'POST'))
def recover():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        dest = db.execute(
            'SELECT email from user where username= ?', (username,)
        ).fetchone()

        if (dest is None):
            abort(404)

        else:
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            sender = secrets.EMAIL
            rec = dest['email']
            s.login(secrets.EMAIL, secrets.PASSWORD)
            password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

            password_reset_url = request.host + '/auth/reset/' + password_reset_serializer.dumps(rec,
                                                                                                 salt='password-reset-salt')
            SUBJECT = 'Password Recovery - Anonymail'
            TEXT = 'Hello {}, \n\nPlease click the link below to reset your password. \n{} \n\nRegards,\nAnonymail'.format(
                username, password_reset_url)
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

            s.sendmail(sender, rec, message)
            return render_template('auth/mailsent.html', user=username)
    else:
        if 'user_id' in session:
            return redirect(url_for('index'))
        else:
            return render_template('auth/recover.html', year=current_year)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, name, email) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), name, email)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    if 'user_id' in session:
        return redirect(url_for('index'))
    else:
        return render_template('auth/register.html', year=current_year)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if 'user_id' in session:
            return redirect(url_for('index'))
        else:
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

            flash(error)
    if 'user_id' in session:
        return redirect(url_for('index'))
    else:
        return render_template('auth/login.html', year=current_year)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/reset/<string:token>', methods=('GET', 'POST'))
def reset(token):
    if request.method == 'POST':
        try:
            password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
            if email is None:
                abort(403)
            password = request.form['password']
            repassword = request.form['repassword']
            if password == repassword:
                db = get_db()
                db.execute('UPDATE user set password = ? where email = ?', (generate_password_hash(password), email))
                db.commit()
                return redirect(url_for('auth.login'))
            else:
                flash('Both passwords are not same')
                return render_template('auth/reset.html')
        except Exception as e:
            abort(403, str(e))

    else:
        return render_template('auth/reset.html', year=current_year)
