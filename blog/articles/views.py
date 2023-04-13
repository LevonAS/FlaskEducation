from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound

# from blog.app import db
# from blog.models import Article, Author
from blog.forms.article import CreateArticleForm


articles_app = Blueprint('articles', __name__, url_prefix='/articles', static_folder='../static')



@articles_app.route('/', methods=['GET'])
def articles_list():
    from blog.models import Article
    articles: Article = Article.query.all()
    return render_template(
        'articles/list.html',
        articles=articles,
    )


@articles_app.route('/<int:article_id>/', methods=['GET'])
def article_detail(article_id):
    from blog.models import Article
    _article: Article = Article.query.filter_by(id=article_id).one_or_none()
    if _article is None:
        raise NotFound
    return render_template(
        'articles/details.html',
        article=_article,
    )


@articles_app.route('/create/', methods=['GET'])
@login_required
def create_article_form():
    form = CreateArticleForm(request.form)
    return render_template('articles/create.html', form=form)


@articles_app.route('/', methods=['POST'])
@login_required
def create_article():
    from blog.app import db
    from blog.models import Article, Author
    form = CreateArticleForm(request.form)
    if form.validate_on_submit():
        _article = Article(title=form.title.data.strip(), text=form.text.data)
        if current_user.author:
            _article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id

        db.session.add(_article)
        db.session.commit()

        return redirect(url_for('articles.article_detail', article_id=_article.id))

    return render_template('articles/create.html', form=form)
