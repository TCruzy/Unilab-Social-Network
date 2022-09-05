
from flask import Flask
from app.extensions import db, migrate, login_manager, csrf
from app.main.views import main_bp
from app.main.api import bp_for_api
import os
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main', 'static')
print('static_folder', static_folder)

BPS = [main_bp, bp_for_api]
# Create Flask application
def create_app():
    app = Flask(__name__)
    app._static_folder = static_folder
    app.config.from_pyfile('config.py')

    register_extensions(app)
    register_blueprints(app)

    return app

# Register extensions
def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'


# Register blueprints
def register_blueprints(application):
    for bp in BPS:
        application.register_blueprint(bp)