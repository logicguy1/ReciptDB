from app import app
from app.models import User, Recipt, Tag, UserTag, Invite

import logging
from logging.handlers import RotatingFileHandler
import os

@app.shell_context_processor
def make_shell_context():
    return {
            'db': db,
            'Recipt': Recipt,
            'Tag': Tag,
            'UserTag': UserTag,
            'Invite': Invite,
        }


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/ReciptDB.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('ReciptDB startup')

