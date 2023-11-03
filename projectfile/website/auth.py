from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm
#new imports:
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a blueprint
auth_bp = Blueprint('auth', __name__)

# Regsitration - allow user to create a new account
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    # When validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.username==uname))
            if user:
                flash('Username already exists, please try another')
                return redirect(url_for('auth.register'))
            # Hash password
            pwd_hash = generate_password_hash(pwd)
            #create a new User
            new_user = User(username=uname, password_hash=pwd_hash, email_id=email)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=register, heading='Register')

# Login - allow user to be authenticated and create event, view booking etc.
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.username == user_name))
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# 
@auth_bp.before_request
def require_login():
    if not current_user.is_authenticated:
        if request.endpoint not in ['auth.login', 'auth.register', 'static']:
            flash("Please log in to access this page.")
            return redirect(url_for('auth.login'))

# Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
