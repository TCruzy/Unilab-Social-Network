
from operator import methodcaller
from flask import Flask
from app.extensions import db, migrate, login_manager, csrf, adminka
from app.main.views import anonymous, change_pfp, change_privacy, check_word, create_post, delete_post, edit_post, following, index, leaderboard, login, logout, main_bp, play_for_earn, search, signup, user_profile, user_settings, users_profile
from app.main.api import bp_for_api, get_balance, like_post
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

    
def register_blueprint_url_views():
    # Register api blueprint url views
    bp_for_api.add_url_rule('/like_post', view_func=like_post)
    bp_for_api.add_url_rule('/get_balance', view_func=get_balance)


    # Register main blueprint url views
    
    main_bp.add_url_rule('/', view_func=index)
    main_bp.add_url_rule('/home', view_func=index)
    main_bp.add_url_rule('/login', methods=['GET', 'POST'], view_func=login)
    main_bp.add_url_rule('/logout', methods=['GET', 'POST'], view_func=logout)
    main_bp.add_url_rule('/signup', methods=['GET', 'POST'], view_func=signup)
    main_bp.add_url_rule('/create-post', methods=['POST'], view_func=create_post)
    main_bp.add_url_rule('/user-profile', view_func=user_profile)
    main_bp.add_url_rule('/user-settings', methods=['GET', 'POST'], view_func=user_settings)
    main_bp.add_url_rule('/users-profile/<int:user_id>', methods=['GET', 'POST'], view_func=users_profile)
    main_bp.add_url_rule('/change_pfp', methods=['GET', 'POST'], view_func=change_pfp)
    main_bp.add_url_rule('/delete_post/<int:post_id>', methods=['GET', 'POST'], view_func=delete_post)
    main_bp.add_url_rule('/change_privacy', methods=['GET', 'POST'], view_func=change_privacy)
    main_bp.add_url_rule('/edit-post/<int:post_id>', methods=['GET', 'POST'], view_func=edit_post)
    main_bp.add_url_rule('/search', methods=['GET', 'POST'], view_func=search)
    main_bp.add_url_rule('/leaderboard', methods=['GET', 'POST'], view_func=leaderboard)
    main_bp.add_url_rule('/following/<int:user_id>', methods=['GET', 'POST'], view_func=following)
    main_bp.add_url_rule('/play-for-earn', methods=['GET', 'POST'], view_func=play_for_earn)
    main_bp.add_url_rule('/check-word/<string:random_word>', methods=['GET', 'POST'], view_func=check_word)
    main_bp.add_url_rule('/anonymous', methods=['GET', 'POST'], view_func=anonymous)
# Register blueprints
def register_blueprints(application):
    
    register_blueprint_url_views()
    
    for bp in BPS:
        application.register_blueprint(bp)
        
def admim_extensions(app):
    adminka.add_view(UserView(User, db.session, name='მომხმარებლები', category='მთავარი მოდელები'))
    adminka.add_view(PostView(Post, db.session, name='პოსტები', category='მთავარი მოდელები'))
    adminka.add_view(LikesView(Like, db.session, name='ლაიქები', category='მთავარი მოდელები'))
    adminka.add_view(FollowsView(Follow, db.session, name='მიმდევრები', category='მთავარი მოდელები'))
    adminka.add_view(FileAdmin(static_folder, '/static/', name='სტატიკური ფაილები'))
    adminka.init_app(app)