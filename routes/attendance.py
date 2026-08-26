from flask import Blueprint, render_template, url_for, redirect, request ,flash
from models.groups import Groups
from models.student_group import StuduentsrGoups
from models.attendance import Attendance
from extinsion import db
from datetime import date, datetime

attendance = Blueprint("attendance", __name__)


@attendance.route("/group/<int:group_id>/attendance", methods=["GET", "POST"])
def take_attendance(group_id):
    group = Groups.query.get_or_404(group_id)
    links = StuduentsrGoups.query.filter_by(group_id=group_id).all()

    if request.method == "POST":
        today = date.today()
        present_ids = request.form.getlist("present")

        for link in links:
            record = Attendance(
                student_id=link.student_id,
                group_id=group_id,
                date=today,
                is_attend=str(link.student_id) in present_ids
            )
            db.session.add(record)

        db.session.commit()
        flash("Attendance saved", "success")
        return redirect(url_for("groups.group_students", group_id=group_id))

    return render_template("take-attendance.html", group=group, links=links, name="take attendance")


@attendance.route("/group/<int:group_id>/attendance/history")
def attendance_history(group_id):
    group = Groups.query.get_or_404(group_id)
    records = Attendance.query.filter_by(group_id=group_id).order_by(Attendance.date.desc()).all()

    sessions = {}
    for record in records:
        sessions.setdefault(record.date, []).append(record)

    return render_template("attendance-history.html", group=group, sessions=sessions, name="attendance history")

@attendance.route("/group/<int:group_id>/attendance/delete/<string:session_date>", methods=["GET", "POST"])
def delete_attendance_session(group_id, session_date):
    parsed_date = datetime.strptime(session_date, "%Y-%m-%d").date()
    Attendance.query.filter_by(group_id=group_id, date=parsed_date).delete()
    db.session.commit()
    flash("Attendance deleted", "success")
    return redirect(url_for("attendance.attendance_history", group_id=group_id))