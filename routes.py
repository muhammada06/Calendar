from flask import Flask, render_template,request,redirect,url_for,flash,session,jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,current_user
from flask_migrate import Migrate
from models import User,Event
import googlemaps

def register_routes(app,db,maps):

    #USER HOME PAGE
    @app.route('/')
    def homepage():
            return render_template('mainPage.html')
    
    @app.route('/FAQs')
    def faqs():
        return render_template('FAQs.html')
    
    @app.route('/calendar')
    def calendar():
        return render_template('calendar.html')
    
    @app.route('/aboutUs')
    def aboutUs():
        return render_template('aboutUs.html')
        
            
    



    @app.route('/addEvent', methods=['POST'])
    def addEvent():
        if request.method=='POST':
            event_name=data.get['name']
            location=data.get['location']
            event_start=data.get['start_time']
            event_end=data.get['end_time']

            try:
                starting_time = datetime.strptime(event_start, '%Y-%m-%dT%H:%M')
                ending_time = datetime.strptime(event_end, '%Y-%m-%dT%H:%M')
            except ValueError:
                return jsonify({"error": "Invalid date format. Please use YYYY-MM-DDTHH:MM"}), 400
        
            if starting_time>=ending_time:
                return jsonify({"error": "Event start time cannot be after end time"}), 400
            
            event_location_check=maps.geocode(location)

            if not event_location_check:
                return jsonify({"error": "Place does not exist"}), 400
            
            createdEvent=Event(event_title=event_name,event_location=location,event_start=starting_time,event_end=ending_time,user_id=current_user.id)
            db.session.add(createdEvent)
            db.session.commit()
            return jsonify({"message": "Event added successfully!"}), 201
    

    # @app.route('/modify_event/<int:event_id>', methods=['GET','POST'])
    # def modifyEvent(event_id):
    #     chosenEvent=Event.query.filter_by(id=event_id).first()

    #     if request.method=='POST':
    #         desired_modification=request.form.get('action')

    #         if desired_modification=='edit':
    #             chosenEvent.event_title=request.form['name']
    #             chosenEvent.event_location=request.form['location']
    #             chosenEvent.event_start=request.form['start_time']
    #             chosenEvent.event_end=request.form['end_time']

    #             try:
    #                 chosenEvent.starting_time = datetime.strptime(chosenEvent.event_start, '%Y-%m-%dT%H:%M')
    #                 chosenEvent.ending_time = datetime.strptime(chosenEvent.event_end, '%Y-%m-%dT%H:%M')
    #             except ValueError:
    #                 flash("Invalid date format. Please use the correct format.", category='error')
    #                 return render_template('modifyEvent.html')
        
    #             if chosenEvent.starting_time>=chosenEvent.ending_time:
    #                 flash("Event start time cannot be after the end time", catagory='error')
    #                 return render_template('modifyEvent.html')
            
    #             event_location_check=maps.geocode(chosenEvent.location)

    #             if not event_location_check:
    #                 flash ("Place does not exist", catagory='error')
    #                 return render_template('modifyEvent.html')
                
    #             db.session.commit()
    #             return redirect(url_for('calendar')) 
            
    #         elif desired_modification=='delete':
    #             db.session.delete(chosenEvent)
    #             db.session.commit()
    #             flash("Deletion completion",catagory='success')
    #             return redirect(url_for('calendar'))
        
    #     return render_template('modifyEvent.html', event=chosenEvent)

    @app.route('/delete_event', methods=['POST'])
    def delete_event():
        data = request.get_json()
        event_title = data.get("title")

        # Find the event in the database for the logged-in user
        event = Event.query.filter_by(event_title=event_title, user_id=current_user.id).first()

        if event:
            db.session.delete(event)
            db.session.commit()
            return jsonify({"success": True})
    
        return jsonify({"success": False, "message": "Event not found"}), 404



    @app.route('/getEvents', methods=['GET'])
    def getEvents():
        events = Event.query.filter_by(user_id=current_user.id).all()
    
    # Convert event objects into JSON format
        events_list = [{
            "name": event.event_title,
            "location": event.event_location,
            "start_time": event.event_start.strftime('%Y-%m-%dT%H:%M'),
            "end_time": event.event_end.strftime('%Y-%m-%dT%H:%M')
        } for event in events]

        return jsonify(events_list)


            


    @app.route('/view_directions/<int:event_id>', methods=['GET','POST'])
    def viewRoute(event_id):
        chosenEvent=Event.query.filter_by(id=event_id).first()

        if request.method=='POST':
            starting_place=request.form['starting_location']
            mode_of_transportation=request.form['mode_of_transportation']
            event_location_check=maps.geocode(starting_place)
            if not event_location_check:
                    flash ("Place does not exist", catagory='error')
                    return render_template('viewDirections.html')
            
        
        iso_format_time=chosenEvent.start_time.isoformat()
        route=maps.directions(starting_place,chosenEvent.event_location,mode=mode_of_transportation,arrival_time=iso_format_time)

        if not route:
            flash("No route found.", category='error')
            return redirect(url_for('calendar'))
        
        if route:
            return render_template('viewDirections.html', event=chosenEvent, route=route)
    
        return render_template('viewDirections.html', event=chosenEvent)
    

    #USER AUTHORIZATION SYSTEM
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
        return render_template('register.html')
        


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
                return redirect(url_for('calendar'))
            else:
                flash('Wrong username/password',category='error')
        return render_template('loginFINAL.html')

        
