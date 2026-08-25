from extinsion import db

class StuduentsrGoups(db.Model):
    __tablename__ = "student_group"
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True )
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), primary_key=True )

    student = db.relationship("Student", backref="student_group")
    group = db.relationship("Groups", backref="student_group")    