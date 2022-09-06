
# Flask application config that need to be set before creating the app
import os

FLASK_ADMIN_SWATCH = 'cerulean'
SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "data.sqlite")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False