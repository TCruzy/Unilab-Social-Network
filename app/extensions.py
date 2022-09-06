
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
login_manager = LoginManager()

adminka = Admin(name='Admin', template_mode='bootstrap4')
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()