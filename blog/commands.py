import click
from werkzeug.security import generate_password_hash





@click.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    from wsgi import app
    from .app import db
    from blog.models import User
    db.create_all()
    print("done!")


@click.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from wsgi import app
    from .app import db
    from blog.models import User
    admin = User(email="admin@fff.com", password=generate_password_hash('masteradmin'), is_staff=True)
    james = User(email="james@fff.com", password=generate_password_hash('masteradmin'))
    mike = User(email="mike@fff.com", password=generate_password_hash('masteradmin'))
    
    db.session.add(admin)
    db.session.add(james)
    db.session.add(mike)
    db.session.commit()
    
    print("done! created users:", admin, james, mike)


@click.command("create-articles")
def create_articles():
    """
    Run in your terminal:
    flask create-articles
    > done! created articles: <Article 1> <Article 2> <Article 3>
    """
    from wsgi import app
    from .app import db
    from blog.models import Article
    a1 = Article(
        title="Flask", 
        text="Flask — фреймворк для создания веб-приложений на языке\
            программирования Python, использующий набор инструментов Werkzeug,\
            а также шаблонизатор Jinja2.", 
        author=1)
    a2 = Article(
        title="Django", 
        text="Django — свободный фреймворк для веб-приложений на языке Python,\
            использующий шаблон проектирования MVC.", 
        author=2)
    a3 = Article(
        title="Django REST", 
        text="Django REST framework - это мощный и гибкий набор инструментов\
            для создания Web API.", 
        author=3)
    
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.commit()
    
    print("done! created articles:", a1, a2, a3)
