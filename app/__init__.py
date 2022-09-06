
from flask import Flask
from app.extensions import db, migrate, login_manager, csrf, adminka
from app.main.views import main_bp
from app.main.api import bp_for_api
from app.admin.views import UserView, PostView, LikesView, FollowsView
from app.main.models import Follow, Post, User, Like
from flask_admin.contrib.fileadmin import FileAdmin
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
    admim_extensions(app)
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
        
def admim_extensions(app):
    adminka.add_view(UserView(User, db.session, name='Users', category='Models'))
    adminka.add_view(PostView(Post, db.session, name='Posts', category='Models'))
    adminka.add_view(LikesView(Like, db.session, name='Likes', category='Models'))
    adminka.add_view(FollowsView(Follow, db.session, name='Follows', category='Models'))
    adminka.add_view(FileAdmin(static_folder, '/static/', name='Static Files'))
    adminka.init_app(app)