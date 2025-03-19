from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask
from app import db 



#Creating a Table for the User and it's information
class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True, nullable=False)
    password= db.Column(db.String(200), nullable=False)

class Event(UserMixin,db.Model):
    __tablename__='events'
    id=db.Column(db.Integer,primary_key=True)
    event_title=db.Column(db.String(100),nullable=False)
    event_date=db.Column(db.Date,nullable=False)
    event_time=db.Column(db.String(50),nullable=False)
    event_location=db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('events', lazy='dynamic'))





