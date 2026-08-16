from extinsion import db

class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50))
    student_num = db.Column(db.String(50))
    parent_num = db.Column(db.String(50))
