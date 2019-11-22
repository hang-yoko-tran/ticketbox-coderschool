from flask import Blueprint, request, url_for, render_template, flash, redirect
from src.models.user import User
from src import db
user_blueprint = Blueprint(
    'user_bp', __name__, template_folder='../../templates')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
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


@user_blueprint.route('/login')
def login():

    return render_template('user/login.html')


@user_blueprint.route('/forgot-password')
def forgot_password():
    return render_template('user/forgot_password.html')
