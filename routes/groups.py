from flask import Blueprint,render_template,url_for,redirect,request
from models.groups import Groups
from extinsion import db

groups=Blueprint("groups",__name__)

@groups.route("/group")
def group():
    group = Groups.query.all()
    return render_template("group.html", group=group, name="Groups")

@groups.route("/group/add", methods=["GET", "POST"])
def add_group():
    if request.method == "POST":
        name = request.form.get("name")
        group=Groups(
            name=name
        )
        db.session.add(group)
        db.session.commit()
        return redirect(url_for("groups.group"))
    return render_template("add-group.html"  ,name="add group")

