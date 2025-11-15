from functools import wraps

from flask import session
from Flask import Blueprint, render_template, request, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def url_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'url_entered' not in session:
            return redirect(url_for('main.passfunc'))
        return f(*args, **kwargs)
    return decorated_function

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass

# Redirect to URL entry if logged in
@main_bp.route('/e')
@login_required
def passfunc():
    session.pop('_flashes', None)
    return redirect(url_for('main.home'))


# Enter video URL
@main_bp.route('/enter_url', methods=['GET', 'POST'])
@login_required
def enter_url():
    pass    

@main_bp.route('submit_url', methods=['GET', 'POST'])
@login_required
@url_required
def submit_url():
    pass


@main_bp.route('index')
@login_required
@url_required
def dashboard():
    pass



