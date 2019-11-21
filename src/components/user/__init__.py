from flask import Blueprint, render_template

user_blueprint = Blueprint('user_bp', __name__, template_folder='../../templates')


@user_blueprint.route('/register')
def register():
    return render_template('user/register.html')

@user_blueprint.route('/login')
def login():
    return render_template('user/login.html')

@user_blueprint.route('/forgot-password')
def forgot_password():
    return render_template('user/forgot_password.html')