from flask import Flask,Blueprint,render_template,url_for,redirect,request
from models.student import Student
from extinsion import db
from models.groups import Groups
from models.student_group import StuduentsrGoups

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
        return redirect(url_for("students.student"))
    return render_template("add-student.html"  ,name="add student")

@students.route("/student/delete/<int:student_id>", methods=["GET", "POST"])
def delete_student( student_id ):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
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
            return redirect(url_for("students.student"))

        new_link = StuduentsrGoups(student_id=student_id, group_id=group_id)
        db.session.add(new_link)
        db.session.commit()

        return redirect(url_for("students.student"))

    return render_template("add-student-group.html", student=student, groups=groups, name="add student to group")
