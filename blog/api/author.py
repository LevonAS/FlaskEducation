from flask_combo_jsonapi import ResourceList, ResourceDetail
from combojsonapi.event.resource import EventsResource

from blog.extensions import db
from blog.models import Author, Article
from blog.schemas import AuthorSchema


class AuthorList(ResourceList):
    schema = AuthorSchema
    data_layer = {
        'session': db.session,
        'model': Author,
    }


class AuthorDetailEvents(EventsResource):

    def event_get_articles_count(self, *args, **kwargs):
        return {'count': Article.query.filter(Article.author_id == kwargs['id']).count()}

        
class AuthorDetail(ResourceDetail):
    events = AuthorDetailEvents
    schema = AuthorSchema
    data_layer = {
        'session': db.session,
        'model': Author,
    }
