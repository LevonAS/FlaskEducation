from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
# from flask_admin import Admin

# from blog.admin.views import CustomAdminIndexView

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

# admin = Admin(
#     index_view=CustomAdminIndexView(),
#     name='Blog Admin Panel',
#     template_mode='bootstrap4',
# )
