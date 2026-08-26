from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("welcome back", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))

        flash("invalid username or password", "error")

    return render_template("login.html", name="login")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logged out", "success")
    return redirect(url_for("auth.login"))
