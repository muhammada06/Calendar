from flask import Flask, render_template,request,redirect,url_for,flash,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate

db=SQLAlchemy()
#IMPORTING FLASK
def create_app():
    app=Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY']='lol'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./calanderdb.db'
    db.init_app(app)
    from routes import register_routes
    register_routes(app,db)


    #imports later on
    migrate=Migrate(app,db)
    return app

 








            





 
    
