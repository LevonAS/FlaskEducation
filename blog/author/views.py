from flask import Blueprint, render_template
import requests

from blog.models import Author


author_app = Blueprint('author', __name__, url_prefix='/author', static_folder='../static')


@author_app.route('/')
def author_list():
    authors = Author.query.all()

    article_count = {}
    for author in authors:
        count_articles: Dict = requests.get(f'http://127.0.0.1:5000/api/articles/{author.user.id}/event_get_count_by_author/').json()
        article_count[author.user.id] = count_articles['count']
   
    return render_template(
        'authors/list.html',
        authors=authors,
        article_count=article_count,
    )
