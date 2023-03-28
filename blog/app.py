from flask import Flask, Blueprint, render_template
from blog.models.database import db
from .user.views import user_app
from .report.views import report_app
from .articles.views import articles_app


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    register_blueprints(app)
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
