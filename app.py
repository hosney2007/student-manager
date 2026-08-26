from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user
from extinsion import db
from routes.student import students
from routes.groups import groups
from routes.attendance import attendance
from routes.auth import auth
from models.student import Student
from models.user import User
from config import Config
import os

app = Flask(__name__)

# app configuration
app.config.from_object(Config)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", Config.SECRET_KEY)

db.init_app(app)

app.register_blueprint(students)
app.register_blueprint(groups)
app.register_blueprint(attendance)
app.register_blueprint(auth)

# --- login manager -----------------------------------------------------
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "please log in to continue"
login_manager.login_message_category = "error"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# any route not in this set requires a logged-in user
PUBLIC_ENDPOINTS = {"auth.login", "static"}


@app.before_request
def require_login():
    if request.endpoint is None:
        return
    if request.endpoint in PUBLIC_ENDPOINTS:
        return
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login", next=request.path))


# --- db setup + first-run admin bootstrap -------------------------------
with app.app_context():
    db.create_all()

    if not User.query.first():
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        admin = User(username=admin_username)
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()


@app.route("/")
def home():
    return render_template("Home.html", name="home")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
