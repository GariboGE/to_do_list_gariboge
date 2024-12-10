from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from forms.forms import LoginForm, RegisterForm
from services.auth_service import create_user, get_user_by_username

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('tasks.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not create_user(form.username.data, form.password.data):
            flash('Username not available, please choose another one', 'warning')
            return redirect(url_for('auth.register'))
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
