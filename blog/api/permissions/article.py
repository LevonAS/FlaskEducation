from datetime import datetime

from combojsonapi.permission.permission_system import (
    PermissionMixin,
    PermissionUser,
    PermissionForGet,
    PermissionForPatch,
)
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user

from blog.models import Article


class ArticleListPermission(PermissionMixin):
    ALL_AVAILABLE_FIELDS = (
        'id',
        'author',
        'title',
        'text',
        'created_at',
        'updated_at',
    )

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:

        if not current_user.is_authenticated:
            raise AccessDenied('No access')

        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)

        return self.permission_for_get


class ArticlePatchPermission(PermissionMixin):
    """
    Example request:
    curl --location --request PATCH 'http://127.0.0.1:5000/api/articles/5' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "data": {
        "type": "article",
        "attributes": {
            "title": "New article",
            "text": "object for experiments 47"
        },
        "id": "5"
    }
    }'
    """
    PATCH_AVAILABLE_FIELDS = [
        "text",
        "title",
    ]

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(self, *args, data: dict = None, obj: Article = None, user_permission: PermissionUser = None,
                   **kwargs) -> dict:
        permission_for_patch = user_permission.permission_for_patch_permission(model=Article)
        
        print('arF', current_user)
        if not current_user.is_authenticated:
            raise AccessDenied('No access')

        if current_user.is_staff or current_user.author.id == obj.author_id:
            res = {
                k: v
                for k, v in data.items()
                if k in permission_for_patch.columns
            }
            res.setdefault("updated_at", datetime.now())
            return res
        else:
            raise AccessDenied("No access")