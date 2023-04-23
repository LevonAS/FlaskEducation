from flask_combo_jsonapi import ResourceList, ResourceDetail
from combojsonapi.event.resource import EventsResource
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user
import requests

from blog.extensions import db
from blog.models import Article
from blog.schemas import ArticleSchema
from blog.api.permissions.article import ArticleListPermission,ArticlePatchPermission


class ArticleListEvent(EventsResource):

    def event_get_count(self, *args, **kwargs):
        return {'count': Article.query.count()}

    def event_get_ip_server(self, *args, **kwargs):
        return {'count': requests.get('https://ifconfig.io/ip').text}


class ArticleList(ResourceList):
    events = ArticleListEvent
    schema = ArticleSchema
    data_layer = {
        'session': db.session,
        'model': Article,
        'permission_get': [ArticleListPermission],
    }


class ArticleDetailEvent(EventsResource):

    def event_get_count_by_author(self, *args, **kwargs):
        return {'count': Article.query.filter(Article.author_id == kwargs['id']).count()}


class ArticleDetail(ResourceDetail):
    events = ArticleDetailEvent
    schema = ArticleSchema
    data_layer = {
        'session': db.session,
        'model': Article,
        # 'permission_get': [ArticleListPermission],
        'permission_patch': [ArticlePatchPermission],
    }
