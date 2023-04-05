from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


auth_app = Blueprint('auth', __name__, static_folder='../static')


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    from blog.models import User

    if request.method == "GET" and current_user.is_authenticated:
        return redirect(url_for('user.profile', pk=current_user.id))
    
    elif request.method == "GET":
        return render_template("auth/login.html")
   
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email:
        return render_template("auth/login.html", error="email not entered")
    
    _user = User.query.filter_by(email=email).first()
    
    if _user is None or not check_password_hash(_user.password, password):
        return render_template(
            "auth/login.html", error=f"no user {email!r} found or wrong password")
    
    login_user(_user)
    return redirect(url_for('user.profile', pk=_user.id))


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for(".login"))


# @auth_app.route("/secret/")
# @login_required
# def secret_view():
#     return "Super secret data"
