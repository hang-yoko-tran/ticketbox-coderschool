from flask import Blueprint, request, url_for, render_template, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from src.models.user import User
from src import db, login_manager
from itsdangerous import URLSafeTimedSerializer
import requests
from src import app


user_blueprint = Blueprint(
    'user_bp', __name__, template_folder='../../templates')


def send_email(token, email, name):
    url = "https://api.mailgun.net/v3/sandbox1c23cd42dd8b4da093bdfd114f176194.mailgun.org/messages"
    response = requests.post(url,
                             auth=("api", app.config['EMAIL_API']),
                             data={"from": "Hang Yoko <hang.yoko.tran@gmail.com>",
                                   "to": [email],
                                   "subject": "Reset Password",
                                   "text": f"Go to http://localhost:5000/user/new-password/{token}"})

    print(response)
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


@user_blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('ACCOUTN DOES NOT EXIST', 'danger')
            return redirect(url_for('user_bp.forgot_password'))
        s = URLSafeTimedSerializer(app.secret_key)
        token = s.dumps(user.email, salt="UMEO")       
        name = f'{user.firstname} {user.lastname}'
        send_email(token, user.email, name)
    return render_template('user/forgot_password.html')

@user_blueprint.route('/new-password/<token>', methods=['GET', 'POST'])
def new_password(token):
    s = URLSafeTimedSerializer(app.secret_key)
    email = s.loads(token, salt="UMEO", max_age=180)
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("INVALID TOKEN", "danger")
        return redirect(url_for('root'))
    if request.method == "POST":
        if request.form['new_password'] != request.form['confirm_password']:
            flash('Password not match!', 'warning')
        user.set_password(request.form['new_password'])
        db.session.commit()
        flash("You have set new password", "successful")
        return redirect(url_for('user_bp.login'))
    return render_template('user/reset_password.html', token=token)