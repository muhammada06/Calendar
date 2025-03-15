from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

#Creation of the database
db=SQLAlchemy()


#Creating a Table for the User and it's information
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(unique=True, nullable=False)
    password= db.Column(db.String(200), nullable=False)

class Event(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    event_title=db.Column(nullable=False)
    event_date=db.Colmmn(db.Date,nullable=False)
    event_time=db.Column(db.String,nullable=False)
    event_location=db.Column(db.String,nullable=False)




