import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOADED_IMAGES_DEST = os.environ.get('UPLOADED_IMAGES_DEST') or 'app/assets/recipts'
    TIME_STR = "%Y-%m-%d %X.%f"
    WORDLIST = "wordlistDK.txt"
    DEBUG = False

    # Wheater or not to use multi threading when handeling images
    QUICK_MODE = False 

    # SQLAlchemy database config, track modifications is set for compadabilaty with SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
