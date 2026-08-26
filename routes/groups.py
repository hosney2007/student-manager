from flask import Blueprint,render_template,url_for,redirect,request,flash
from models.groups import Groups
from extinsion import db
from models.student_group import StuduentsrGoups

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
        flash("group created", "success")
        return redirect(url_for("groups.group"))
    return render_template("add-group.html"  ,name="add group")

@groups.route("/group/<int:group_id>")
def group_students(group_id):
    group = Groups.query.get_or_404(group_id)
    links = StuduentsrGoups.query.filter_by(group_id=group_id).all()
    return render_template("group-students.html", group=group, links=links, name="group students")


@groups.route("/group/<int:group_id>/edit", methods=["GET", "POST"])
def edit_group(group_id):
    group = Groups.query.get_or_404(group_id)

    if request.method == "POST":
        group.name = request.form.get("name")
        db.session.commit()
        flash("group updated", "success")
        return redirect(url_for("groups.group"))

    return render_template("edit-group.html", group=group, name="edit group")

