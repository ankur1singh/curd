from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from flask_login import UserMixin

db=SQLAlchemy()

class User(UserMixin,db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(200),nullable=False)
    email= db.Column(db.String(200),nullable=False)
    mobile = db.Column(db.Integer(),nullable=False)
    password = db.Column(db.String(300),nullable=False)
    profiles = db.relationship('Profile', backref='User',lazy=True)

    def __repr__(self) -> str:
        return f"{self.name} - {self.password}"


class Profile(db.Model):
    profile_id=db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(200),nullable=False)
    email= db.Column(db.String(200),nullable=False)
    mobile = db.Column(db.Integer(),nullable=False)
    dob = db.Column(db.Date(),nullable=False)
    gender = db.Column(db.String(200),nullable=False)
    education = db.Column(db.String(200),nullable=False)
    image = db.Column(db.String(200),nullable=False)
    skill_id= db.Column(db.Integer, db.ForeignKey('skill.id'))
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"{self.profile_id}"

    class skill(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        title= db.Column(db.String(200),nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"