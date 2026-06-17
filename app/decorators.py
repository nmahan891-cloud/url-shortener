from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def login_required_custom(message='لطفاً وارد شوید.'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(message, 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator