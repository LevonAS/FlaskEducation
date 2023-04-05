from flask_login import UserMixin
from .app import db
from datetime import datetime
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(127))
    is_staff = db.Column(db.Boolean, default=False)
    # articles = relationship('Article')
    
    def __repr__(self):
        return f"<User #{self.id} {self.email!r}>"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(127), nullable=False)
    text = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
        
    def __repr__(self):
        return f"<AArticle #{self.id} {self.title!r}>"
        # return f"<Article %r #{self.id}>"