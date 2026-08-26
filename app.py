from flask import Flask , render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from extinsion import db
from routes.student import students
from routes.groups import groups
from models.student import Student
from routes.attendance import attendance
from config import Config
import os

app=Flask(__name__)
app.register_blueprint(students)
app.register_blueprint(groups)
app.register_blueprint(attendance)

#app configrtion==//
app.config["SECRET_KEY"] = "YOUR SECRET KEY"
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("Home.html",name="home")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")