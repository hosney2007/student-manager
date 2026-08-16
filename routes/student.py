from flask import Flask,Blueprint,render_template,url_for,redirect,request
from models.student import Student
from extinsion import db

students=Blueprint("students",__name__)

@students.route("/student")
def student():
    student = Student.query.all()
    return render_template("student.html", student=student, name="students")

@students.route("/student/add", methods=["GET", "POST"])
def add_student():
    if request.method == "post":
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

