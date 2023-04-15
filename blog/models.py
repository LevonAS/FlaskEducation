from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

from blog.extensions import db


article_tag_associations_table = Table(
    'article_tag_association',
    db.metadata,
    db.Column('article_id', db.Integer, ForeignKey('articles.id'), nullable=False),
    db.Column('tag_id', db.Integer, ForeignKey('tags.id'), nullable=False),
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    first_name = db.Column(db.String(127))
    last_name = db.Column(db.String(127))
    password = db.Column(db.String(127))
    is_staff = db.Column(db.Boolean, default=False)

    author = relationship('Author', uselist=False, back_populates='user')
    
    def __repr__(self):
        return f"<User #{self.id} {self.email!r}>"

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='author')
    articles = relationship('Article', back_populates='author')

    def __str__(self):
        return self.user.email


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'), nullable=False)
    title = db.Column(db.String(127), nullable=False)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    author = relationship('Author', back_populates='articles')
    tags = relationship('Tag', secondary=article_tag_associations_table, back_populates='articles')

    # def __repr__(self):
    #     return f"<Article #{self.id} {self.title!r}>"
        # return f"<Article %r #{self.id}>"

    def __str__(self):
        return self.title 
    
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)

    articles = relationship('Article', secondary=article_tag_associations_table, back_populates='tags')

    def __str__(self):
        return self.name