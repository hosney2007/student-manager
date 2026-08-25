from extinsion import db

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_attend = db.Column(db.Boolean, default=False)

    student = db.relationship("Student")
