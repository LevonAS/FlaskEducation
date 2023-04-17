from flask_admin.contrib.sqla import ModelView

def register_views():
    from blog import models
    from blog.admin.views import TagAdminView, UserAdminView, ArticleAdminView
    from blog.extensions import admin, db

    admin.add_view(ArticleAdminView(models.Article, db.session, name='Статьи'))
    admin.add_view(TagAdminView(models.Tag, db.session, name='Теги'))
    admin.add_view(UserAdminView(models.User, db.session, name='Пользователи'))
    # admin.add_view(ModelView(models.Author, db.session, name='Авторы'))
    
