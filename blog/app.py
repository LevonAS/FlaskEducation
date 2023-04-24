from flask import Flask, Blueprint, render_template
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash
from combojsonapi.spec import ApiSpecPlugin
from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin
import click

from blog.extensions import app, db, login_manager, migrate, csrf, admin, api
from .user.views import user_app
from .report.views import report_app
from .articles.views import articles_app
from .author.views import author_app
from .tags.views import tags_app
from .auth.views import auth_app
from blog import admin as admmin_view
from blog import commands


def create_app() -> Flask:
    # app = Flask(__name__)
    app.config.from_object('blog.config')
    
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    # csrf.init_app(app)
    admin.init_app(app)

    api.plugins = [
        EventPlugin(),
        PermissionPlugin(),
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]
    api.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from blog.models import User
        return User.query.get(int(user_id))
    
    register_blueprints(app)
    register_commands(app)
    register_api_routes()

    return app

index_app = Blueprint('index', __name__, static_folder='../static', url_prefix='/')

@index_app.route("/")
def index_view():
    return render_template("index.html")


def register_api_routes():
    from blog.api.tag import TagList, TagDetail
    from blog.api.user import UserList, UserDetail
    from blog.api.author import AuthorList, AuthorDetail
    from blog.api.article import ArticleList, ArticleDetail

    api.route(TagList, 'tag_list', '/api/tags/', tag='Tag')
    api.route(TagDetail, 'tag_detail', '/api/tags/<int:id>', tag='Tag')

    api.route(UserList, 'user_list', '/api/users/', tag='User')
    api.route(UserDetail, 'user_detail', '/api/users/<int:id>', tag='User')

    api.route(AuthorList, 'author_list', '/api/authors/', tag='Author')
    api.route(AuthorDetail, 'author_detail', '/api/authors/<int:id>', tag='Author')

    api.route(ArticleList, 'article_list', '/api/articles/', tag='Article')
    api.route(ArticleDetail, 'article_detail', '/api/articles/<int:id>', tag='Article')


def register_blueprints(app: Flask):
    app.register_blueprint(index_app)
    app.register_blueprint(user_app)
    app.register_blueprint(report_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(author_app)
    app.register_blueprint(tags_app)
    app.register_blueprint(auth_app)
    admmin_view.register_views()


def register_commands(app: Flask):
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_users)
    app.cli.add_command(commands.create_tags)
    app.cli.add_command(commands.create_articles)

