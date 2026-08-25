from extinsion import db

class Groups(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50))
    

