#!/usr/bin/env python
"""User routes"""
from flask import Blueprint, request, render_template, make_response, flash, redirect, url_for
from app.models.user import User
from app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from app.forms.user_forms import RegistrationForm, LoginForm


users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['POST'])
def register():
    """Create a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('landing.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('landing.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('landing.index'))

@users_blueprint.route('/delete', methods=['POST'])
@login_required
def delete():
    """Delete user"""
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'info')
    return redirect(url_for('landing.index'))

# @users_blueprint.route('/<string:user_id>/')
# def profile(user_id):
#     user = User.query.get_or_404(user_id)
#     return render_template('users/profile.html', user=user)