from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import NotFound
from ..user.views import USERS


articles_app = Blueprint('articles', __name__, static_folder='../static', url_prefix='/articles')

ARTICLES = {
    1: {
        'title': 'Flask',
        'text': 'Flask — фреймворк для создания веб-приложений на языке\
            программирования Python, использующий набор инструментов Werkzeug,\
            а также шаблонизатор Jinja2',
        'author': 1
    },
    2: {
        'title': 'Django',
        'text': 'Django — свободный фреймворк для веб-приложений на языке Python,\
            использующий шаблон проектирования MVC',
        'author': 2
    },
    3: {
        'title': 'Django REST',
        'text': 'Django REST framework - это мощный и гибкий набор инструментов\
            для создания Web API.',
        'author': 3
    },
}

# ARTICLES = ["Flask", "Django", "JSON:API"]

@articles_app.route('/')
def articles_list():
    return render_template(
        'articles/list.html',
        articles=ARTICLES,
    )

@articles_app.route('/<int:pk>')
def get_article(pk: int):
    try:
        article=ARTICLES[pk]
    except KeyError:
        # return redirect('/articles/')
        raise NotFound(f'Article id {pk} not found')
    return render_template(
        'articles/details.html',
        article=article,
        users=USERS,
    )