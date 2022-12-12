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

from app.bps.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

from app.bps.tags import bp as tags_bp
app.register_blueprint(tags_bp, url_prefix="/tags")

from app.bps.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix="/api")

from app.bps.dashboard import bp as dash_bp
app.register_blueprint(dash_bp)

from app.bps.stats import bp as stats_bp
app.register_blueprint(stats_bp, url_prefix="/stats")

from app.bps.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix="/admin")

from app import models
