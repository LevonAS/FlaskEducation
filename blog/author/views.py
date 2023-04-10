from flask import Blueprint, render_template



author_app = Blueprint('author', __name__, url_prefix='/author', static_folder='../static')


@author_app.route('/')
def author_list():
    from blog.models import Author
    authors = Author.query.all()
    return render_template(
        'authors/list.html',
        authors=authors,
    )
