from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import joinedload

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
    _article: Article = Article.query.filter_by(
        id=article_id
    ).options(
        joinedload(Article.tags)
    ).one_or_none()
    
    if _article is None:
        raise NotFound
    return render_template(
        'articles/details.html',
        article=_article,
    )


@articles_app.route('/create/', methods=['GET'])
@login_required
def create_article_form():
    from blog.models import Tag
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    return render_template('articles/create.html', form=form)


@articles_app.route('/', methods=['POST'])
@login_required
def create_article():
    from blog.app import db
    from blog.models import Article, Author, Tag
    
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    
    if form.validate_on_submit():
        _article = Article(title=form.title.data.strip(), text=form.text.data)
        if current_user.author:
            _article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id
        
        print('AVw_1', form.tags.data)
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            print('AVw_2', selected_tags)
            for tag in selected_tags:
                print('AVw_3', tag)
                _article.tags.append(tag)

        print('AVw_4', _article.id, _article.text, _article.author_id,  _article.tags)
        db.session.add(_article)
        db.session.commit()

        return redirect(url_for('articles.article_detail', article_id=_article.id))

    return render_template('articles/create.html', form=form)
