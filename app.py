from flask import Flask, render_template,request,redirect,url_for,flash,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager
from flask_migrate import Migrate
import googlemaps


db=SQLAlchemy()
#IMPORTING FLASK
def create_app():
    app=Flask(__name__, template_folder='templates')
    login=LoginManager()
    login=LoginManager(app)
    app.config['SECRET_KEY']='lol'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./calanderdb.db'
    app.config['GOOGLE_MAPS_API_KEY'] = 'AIzaSyAZG1EHE7K9ncRou7nZrbxR7MMLuZJMzrM' 
    gmaps = googlemaps.Client(key=app.config['GOOGLE_MAPS_API_KEY'])
    db.init_app(app)
    from routes import register_routes
    register_routes(app,db,gmaps)


    #imports later on
    migrate=Migrate(app,db)

    @login.user_loader
    def load_user(id):
        from models import User
        return User.query.get(int(id))
    
    return app


 
