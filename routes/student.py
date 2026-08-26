from flask import Flask,Blueprint,render_template,url_for,redirect,request,flash
from models.student import Student
from extinsion import db
from models.groups import Groups
from models.student_group import StuduentsrGoups
from models.attendance import Attendance

students=Blueprint("students",__name__)

@students.route("/student")
def student():
    student = Student.query.all()
    return render_template("student.html", student=student, name="students")

@students.route("/student/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        student_num = request.form.get("student_num")
        parent_num = request.form.get("parent_num")
        studet=Student(
            name=name,
            student_num=student_num,
            parent_num=parent_num
        )
        db.session.add(studet)
        db.session.commit()
        flash("student registred", "success")
        return redirect(url_for("students.student"))
    return render_template("add-student.html"  ,name="add student")

@students.route("/student/delete/<int:student_id>", methods=["GET", "POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)

    in_group = StuduentsrGoups.query.filter_by(student_id=student_id).first()
    has_attendance = Attendance.query.filter_by(student_id=student_id).first()

    if in_group or has_attendance:
        flash("can't delete this student — remove them from their group(s) first", "error")
        return redirect(url_for("students.student"))

    db.session.delete(student)
    db.session.commit()
    flash("student deleted", "success")
    return redirect(url_for("students.student"))


@students.route("/student/<int:student_id>/add-group", methods=["GET", "POST"])
def add_student_to_group(student_id):
    student = Student.query.get_or_404(student_id)
    groups = Groups.query.all()

    if request.method == "POST":
        group_id = request.form.get("group_id")

        # نتأكد إن الطالب ده مش مضاف في المجموعة دي قبل كده
        existing = StuduentsrGoups.query.filter_by(
            student_id=student_id,
            group_id=group_id
        ).first()

        if existing:
            flash("student already in this group", "error")
            return redirect(url_for("students.student"))

        new_link = StuduentsrGoups(student_id=student_id, group_id=group_id)
        db.session.add(new_link)
        db.session.commit()
        group_name = new_link.group.name
        flash(f"student added to {group_name} ", "success")
        return redirect(url_for("students.student"))

    return render_template("add-student-group.html", student=student, groups=groups, name="add student to group")

@students.route("/student/<int:student_id>/remove-group/<int:group_id>", methods=["GET", "POST"])
def remove_student_from_group(student_id, group_id):
    link = StuduentsrGoups.query.filter_by(student_id=student_id, group_id=group_id).first_or_404()
    db.session.delete(link)
    db.session.commit()
    flash("student removed from group", "success")
    return redirect(url_for("groups.group_students", group_id=group_id))

