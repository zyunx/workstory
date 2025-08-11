import uuid
import functools

from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app, flash, session, g
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    is_login = session.get('is_login')

    if is_login is None:
        g.is_login = False
    else:
        g.is_login = True


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.is_login:
            return redirect(url_for('auth.login', next=request.path))

        return view(**kwargs)

    return wrapped_view

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password != current_app.config['APP_PASSWORD']:
            do_logout()
            flash('Invalid password.', 'error')
        else:
            do_login()
            next = request.args.get('next', url_for('auth.login_success'))
            return redirect(next)
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    do_logout()
    return redirect(url_for('auth.login'))

@bp.route('/login_success', methods=('GET',))
@login_required
def login_success():
    return render_template('auth/login_success.html') 


def do_login():
    session.clear()
    session['is_login'] = True

def do_logout():
    session.clear()

