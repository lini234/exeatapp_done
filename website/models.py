from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    surname = db.Column(db.String(150))
    otherNames = db.Column(db.String(150))
    matricNumber = db.Column(db.String(11), unique=True)
    password = db.Column(db.String(150))
    department = db.Column(db.String(150))
    college = db.Column(db.String(150))
    level = db.Column(db.Integer)
    exeat = db.Relationship('Exeat')

class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    fullName = db.Column(db.String(150))
    password = db.Column(db.String(150))

class Exeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(150))
    otherNames = db.Column(db.String(150))
    matricNumber = db.Column(db.String(11))
    department = db.Column(db.String(150))
    college = db.Column(db.String(150))
    level = db.Column(db.Integer)
    exeat_date = db.Column(db.String)
    return_date = db.Column(db.String)
    reason = db.Column(db.String(2000))
    address = db.Column(db.String(2000))
    parentsNumber = db.Column(db.String(11))
    status = db.Column(db.String(20))
    today_date = db.Column(db.String(20))
    today_time = db.Column(db.String(20))
    user_id = db.Column(db.String(11), db.ForeignKey('user.id'))