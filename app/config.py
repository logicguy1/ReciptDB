import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "you-will-never-guess"
    UPLOADED_IMAGES_DEST = "app/assets/uploads"
    TIME_STR = "%Y-%m-%d %X"
    WORDLIST = "wordlistDK.txt"
    DEBUG = False
    VERSION = "0.1"
    NGINX_LOGS = "_tests/access.log"
    # NGINX_LOGS = "/var/log/nginx/access.log"

    # SQLAlchemy database config, track modifications is set for compadabilaty with SQLite
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    # SQLALCHEMY_DATABASE_URI = "mysql://user:pwsswd@localhost:3306/reciptdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
