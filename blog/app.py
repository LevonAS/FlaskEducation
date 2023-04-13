from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from sqlalchemy import Table
from werkzeug.security import generate_password_hash
import click

from blog.extensions import migrate
from .user.views import user_app
from .report.views import report_app
from .articles.views import articles_app
from .author.views import author_app
from .tags.views import tags_app
from .auth.views import auth_app
# from blog import commands
# from .commands import init_db

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')

    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SECRET_KEY"] = b"d[12;/[d/2rqpl20rk02KPWDMK923#5U_))%FqwKO^A"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
    
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from blog.models import User
        return User.query.get(int(user_id))
    
    register_blueprints(app)
    register_commands(app)
    
    # with app.app_context():
    #     from .commands import init_db
    return app

index_app = Blueprint('index', __name__, static_folder='../static', url_prefix='/')

@index_app.route("/")
def index_view():
    return render_template("index.html")


def register_blueprints(app: Flask):
    app.register_blueprint(index_app)
    app.register_blueprint(user_app)
    app.register_blueprint(report_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(author_app)
    app.register_blueprint(tags_app)
    app.register_blueprint(auth_app)


def register_commands(app: Flask):
    app.cli.add_command(init_db)
    app.cli.add_command(create_users)
    app.cli.add_command(create_articles)
    app.cli.add_command(create_tags)


@click.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    from blog.models import User
    db.create_all()
    print("done!")


@click.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from blog.models import User
    admin = User(email="admin@fff.com", first_name="admin", last_name="fff", password=generate_password_hash('masteradmin'), is_staff=True)
    james = User(email="james@fff.com", first_name="james", last_name="fff", password=generate_password_hash('masteradmin'))
    mike = User(email="mike@fff.com", first_name="mike", last_name="fff", password=generate_password_hash('masteradmin'))
    
    db.session.add(admin)
    db.session.add(james)
    db.session.add(mike)

    from blog.models import Author
    db.session.add(Author(user_id=1))
    db.session.add(Author(user_id=2))
    db.session.add(Author(user_id=3))

    db.session.commit()
    
    print("done! created users:", admin, james, mike)


@click.command("create-articles")
def create_articles():
    """
    Run in your terminal:
    flask create-articles
    > done! created articles: <Article 1> <Article 2> <Article 3>
    """

    from blog.models import Article, Author, Tag
    a1 = Article(
        title="Flask", 
        text="Flask — фреймворк для создания веб-приложений на языке\
            программирования Python, использующий набор инструментов Werkzeug,\
            а также шаблонизатор Jinja2.", 
        author_id=1)
    a2 = Article(
        title="Django", 
        text="Django — свободный фреймворк для веб-приложений на языке Python,\
            использующий шаблон проектирования MVC.", 
        author_id=2,
        # tags=[4],
        )
    # a2.tags.append(Tag.query.filter_by(id=2))
    # a2.tags.append(Tag.query.filter(Tag.id.in_([2])))
    a3 = Article(
        title="Django REST", 
        text="Django REST framework - это мощный и гибкий набор инструментов\
            для создания Web API.", 
        author_id=3)
    a4 = Article(
        title="MySQL", 
        text="MySQL — свободная реляционная система управления базами данных.\
          Разработку и поддержку MySQL осуществляет корпорация Oracle, получившая\
          права на торговую марку вместе с поглощённой Sun Microsystems, которая \
          ранее приобрела шведскую компанию MySQL AB.", 
        author_id=3)
    
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.add(a4)

    db.session.commit()
    
    print("done! created articles:", a1, a2, a3, a4)


@click.command('create-tags')
def create_tags():
    """
    Run in your terminal:
    flask create-tags
    > Created tags: flask, django, DRF, gb, sqlite, python
    """
    from blog.models import Tag
    from wsgi import app


    with app.app_context():
        tags = ('flask', 'django', 'DRF', 'gb', 'sqlite', 'python')
        for item in tags:
            db.session.add(Tag(name=item))
        db.session.commit()
    click.echo(f'Created tags: {", ".join(tags)}')
