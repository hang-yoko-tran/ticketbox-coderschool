
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from src.models.user import User
migrate = Migrate(app, db)


from src.components.user  import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

@app.route('/')
def root():
    return "Hello from ticket box"
