import click
from werkzeug.security import generate_password_hash

from blog.models import User, Article, Author, Tag
from blog.extensions import app, db


@click.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@click.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    admin = User(email="admin@fff.com", first_name="admin", last_name="fff", password=generate_password_hash('masteradmin'), is_staff=True)
    james = User(email="james@fff.com", first_name="james", last_name="fff", password=generate_password_hash('masteradmin'))
    mike = User(email="mike@fff.com", first_name="mike", last_name="fff", password=generate_password_hash('masteradmin'))
    
    db.session.add(admin)
    db.session.add(james)
    db.session.add(mike)

    db.session.add(Author(user_id=1))
    db.session.add(Author(user_id=2))
    db.session.add(Author(user_id=3))

    db.session.commit()
    
    print("done! created users:", admin, james, mike)


@click.command("create-articles")
def create_articles():
    """
    Run in your terminal:
    flask create-articles
    > done! created articles: <Article 1> <Article 2> <Article 3>
    """

    a1 = Article(
        title="Flask", 
        text="Flask — фреймворк для создания веб-приложений на языке\
            программирования Python, использующий набор инструментов Werkzeug,\
            а также шаблонизатор Jinja2.", 
        author_id=1)
    a2 = Article(
        title="Django", 
        text="Django — свободный фреймворк для веб-приложений на языке Python,\
            использующий шаблон проектирования MVC.", 
        author_id=2,
        # tags=[4],
        )
    # a2.tags.append(Tag.query.filter_by(id=2))
    # a2.tags.append(Tag.query.filter(Tag.id.in_([2])))
    a3 = Article(
        title="Django REST", 
        text="Django REST framework - это мощный и гибкий набор инструментов\
            для создания Web API.", 
        author_id=3)
    a4 = Article(
        title="MySQL", 
        text="MySQL — свободная реляционная система управления базами данных.\
          Разработку и поддержку MySQL осуществляет корпорация Oracle, получившая\
          права на торговую марку вместе с поглощённой Sun Microsystems, которая \
          ранее приобрела шведскую компанию MySQL AB.", 
        author_id=3)
    
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.add(a4)

    db.session.commit()
    
    print("done! created articles:", a1, a2, a3, a4)


@click.command('create-tags')
def create_tags():
    """
    Run in your terminal:
    flask create-tags
    > Created tags: flask, django, DRF, gb, sqlite, python
    """
    with app.app_context():
        tags = ('flask', 'django', 'DRF', 'gb', 'sqlite', 'python')
        for item in tags:
            db.session.add(Tag(name=item))
        db.session.commit()
    click.echo(f'Created tags: {", ".join(tags)}')
