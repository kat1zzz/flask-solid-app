from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_app.config import Config
from dotenv import load_dotenv

load_dotenv()


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)


    from flask_app.main.routes import user
    app.register_blueprint(user)

    return app

