from flask import Flask

from app.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

from app.tags import bp as tags_bp
app.register_blueprint(tags_bp)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix="/api")

from app.dashboard import bp as dash_bp
app.register_blueprint(dash_bp)

from app import models
