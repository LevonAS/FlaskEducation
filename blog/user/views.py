from flask import Blueprint, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.exceptions import NotFound



user_app = Blueprint('user', __name__, static_folder='../static', url_prefix='/users')

# USERS =  ['Bob', 'Alice', 'John']
# USERS = {
#     1: "James",
#     2: "Brian",
#     3: "Peter",
# }


@user_app.route('/')
def user_list():
    from blog.models import User
    users = User.query.all()
    return render_template(
        'users/list.html',
        users=users,
    )


@user_app.route('/<int:pk>')
@login_required
def profile(pk: int):
    from blog.models import User
    _user = User.query.filter_by(id=pk).one_or_none()
    if _user is None:
        raise NotFound(f"User #{pk} doesn't exist!")

    return render_template(
        'users/profile.html',
        user=_user,
    )