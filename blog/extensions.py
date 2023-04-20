from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_combo_jsonapi import Api

from blog.admin.views import CustomAdminIndexView


app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
api = Api()

admin = Admin(
    index_view=CustomAdminIndexView(),
    name='Админ-панель блога',
    template_mode='bootstrap4',
)
