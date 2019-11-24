
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.config.from_object('config.Config')


db = SQLAlchemy(app)
login_manager = LoginManager(app)

from src.models.user import User
migrate = Migrate(app, db)

db.create_all()


from src.controllers.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/')
def root():
    return render_template('index.html')
