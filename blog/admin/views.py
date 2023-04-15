from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for


class CustomAdminView(ModelView):

    def create_blueprint(self, admin):
        blueprint = super().create_blueprint(admin)
        blueprint.name = f'{blueprint.name}_admin'
        return blueprint

    def get_url(self, endpoint, **kwargs):
        if not (endpoint.startswith('.') or endpoint.startswith('admin.')):
            endpoint = endpoint.replace('.', '_admin.')
        return super().get_url(endpoint, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login'))


class CustomAdminIndexView(AdminIndexView):

    # проверка прав доступа к главной странице админки
    @expose()
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for('auth.login'))
        return super().index()


class TagAdminView(CustomAdminView):
    column_searchable_list = ('name',)
    # column_filters = ("name",)
    can_export = True
    export_types = ["csv", "xlsx"]
    create_modal = True
    edit_modal = True
    

class ArticleAdminView(CustomAdminView):
    can_export = True
    export_types = ('csv', 'xlsx')
    column_filters = ('author_id', 'title', 'text')
    column_list = ('author', 'title', 'text', 'tags')
    column_editable_list = ('text', 'tags')
    # column_searchable_list = ('text')



class UserAdminView(CustomAdminView):
    column_exclude_list = ("password",)
    column_details_exclude_list = ('password',)
    column_export_exclude_list = ('password',)
    column_searchable_list = ("first_name", "last_name",  "is_staff", "email")
    column_filters = ("first_name", "last_name", "is_staff", "email")
    column_editable_list = ("first_name", "last_name", "is_staff")
    can_create = False
    can_edit = True
    # can_delete = False