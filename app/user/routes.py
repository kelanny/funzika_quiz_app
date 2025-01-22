#!/usr/bin/env python
"""User routes"""

from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.user.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.user.forms import RegistrationForm, LoginForm


user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    """Register new user."""
    if current_user.is_authenticated:
        return redirect(url_for('main.landing'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
            ).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! \
              You are now able to log in', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', title='Register', form=form)


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    """Log in user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page \
                else redirect(url_for('main.landing'))
        else:
            flash('Login Unsuccessful. \
                  Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@user_bp.route("/logout")
def logout():
    """Logout user account"""
    logout_user()
    return redirect(url_for('main.landing'))


@user_bp.route("/delete_account")
@login_required
def delete_account():
    """Delete user from the database"""
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('main.landing'))
    return render_template('delete_account.html', title='Delete Account')


@user_bp.route('/profile', methods=['GET'])
@login_required
def user_profile():
    """Render the user's profile page."""
    return render_template('profile.html', user=current_user)
