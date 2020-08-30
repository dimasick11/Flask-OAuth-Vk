import os

from dotenv import load_dotenv
load_dotenv()


def initialization_config(app):
    app.config['SECRET_KEY'] = 'top secret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['OAUTH_CREDENTIALS'] = {
    'vk': {
        'id': os.getenv('APP_ID'),
        'secret': os.getenv('SECRET_KEY')
        },
    }
