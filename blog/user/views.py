from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import NotFound



user_app = Blueprint('user', __name__, static_folder='../static', url_prefix='/users')

# USERS =  ['Bob', 'Alice', 'John']
USERS = {
    1: "James",
    2: "Brian",
    3: "Peter",
}


@user_app.route('/')
def user_list():
    return render_template(
        'users/list.html',
        users=USERS,
    )


@user_app.route('/<int:pk>')
def get_user(pk: int):
    try:
        user_name=USERS[pk]
    except KeyError:
        # return redirect('/users/')
        raise NotFound(f'User id {pk} not found')
    return render_template(
        'users/details.html',
        user_name=user_name,
    )