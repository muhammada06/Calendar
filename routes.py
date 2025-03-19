from flask import Flask, render_template,request,redirect,url_for,flash,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from models import User,Event

def register_routes(app,db):
    @app.route('/')
    def homepage():
        if 'user' in session:
            return render_template('index.html', username=session['user'], logged_in=True)
        else:
            return render_template('index.html', logged_in=False)
    
    @app.route('/register',methods=['GET','POST'])
    def register():
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            confirm_password=request.form['confirm_password']
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username Already Exists', category='error')

            if confirm_password!=password:
                flash('Passwords do not match', category='error')
        
            if not existing_user and confirm_password==password:
                new_user = User(username=username, password=password)  
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful!', category='success')
                return redirect (url_for('login')) 
        return render_template('registration.html')
        
            
        


    @app.route('/calendar')
    def calendar():
        return render_template('calendar.html')
    

    

    







    @app.route('/logout')
    def logout():
        session.pop('user',None)
        return render_template('logout.html')
        



    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']

        
            user = User.query.filter_by(username=username).first()
            if user and user.password==password:
                session['user']=username
                return redirect(url_for('homepage'))
            else:
                flash('Wrong username/password',category='error')
        return render_template('login.html')

        
