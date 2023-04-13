from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import joinedload

# from blog.app import db
# from blog.models import Article, Author
from blog.forms.article import CreateArticleForm


tags_app = Blueprint('tags', __name__, url_prefix='/tags', static_folder='../static')
articles_app = Blueprint('articles', __name__, url_prefix='/articles', static_folder='../static')


@tags_app.route('/', methods=['GET'])
def tags_list():
    from blog.models import Tag
    tags: Tag = Tag.query.all()
    return render_template(
        'tags/list.html',
        tags=tags,
    )


@tags_app.route('/<int:tag_id>/', methods=['GET'])
def tag_detail(tag_id):
    from blog.models import Tag
    from blog.models import Article
    _tag: Tag = Tag.query.filter_by(
        id=tag_id
    ).one_or_none()
    # print('TgVw', _tag)
    if _tag is None:
        raise NotFound
    return render_template(
        'tags/details.html',
        tag=_tag,
    )
