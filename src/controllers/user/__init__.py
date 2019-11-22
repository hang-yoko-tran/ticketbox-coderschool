from flask import Blueprint, request, url_for, render_template, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from src.models.user import User
from src import db, login_manager
user_blueprint = Blueprint(
    'user_bp', __name__, template_folder='../../templates')


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        check_email = User.query.filter_by(email=email).first()
        if check_email:
            flash('Email is already exist!', 'warning')
        else:
            new_user = User(
                email=email, firstname=firstname, lastname=lastname)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully create an account and logged in', 'success')
            return redirect(url_for('user_bp.login'))
    return render_template('user/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email does not exist!", 'warning')
        else:
            if not user.check_password(password):
                flash('Invalid email or password', 'danger')
            else:
                login_user(user)
                flash(f'Welcome back {current_user.email}!', 'success')
                return redirect(url_for('root'))
    return render_template('user/login.html')


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))


@user_blueprint.route('/forgot-password')
def forgot_password():
    return render_template('user/forgot_password.html')
