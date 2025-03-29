from flask import Flask, render_template,request,redirect,url_for,flash,session,jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,current_user,login_user,logout_user
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
    
    @app.route('/aboutUs')
    def aboutUs():
        return render_template('aboutUs.html')
    
    @app.route('/calendar')
    def calendar():
        events = Event.query.filter_by(user_id=current_user.id).all()
        event_list = [
        {
            "day": event.event_start.day,
            "month": event.event_start.month,
            "year": event.event_start.year,
            "events": [{
                "id":event.id,
                "title": event.event_title,
                "time": f"{event.event_start.strftime('%I:%M %p')} - {event.event_end.strftime('%I:%M %p')}",
                "location": event.event_location
            }]
        } for event in events
    ]
        return render_template('calendar.html', events=event_list)
    

    

    
    @app.route('/addEvent', methods=['GET', 'POST'])
    def addEvent():
        if request.method == 'POST':
            event_name = request.form['name']
            location = request.form['location']
            event_start = request.form['start_time']
            event_end = request.form['end_time']

            try:
                starting_time = datetime.strptime(event_start, '%Y-%m-%dT%H:%M')
                ending_time = datetime.strptime(event_end, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash("Invalid date format. Please use the correct format.", category='error')
                return render_template('addEvent.html')

            if starting_time >= ending_time:
                flash("Event start time cannot be after the end time", category='error')
                return render_template('addEvent.html')

        # Geocoding location check using a mapping service (like Google Maps API)
            event_location_check = maps.geocode(location)

            if not event_location_check:
                flash("Place does not exist", category='error')
                return render_template('addEvent.html')

        # Create new event instance and store it in the database
            createdEvent = Event(
                event_title=event_name,
                event_location=location,
                event_start=starting_time,
                event_end=ending_time,
                user_id=current_user.id
            )
            db.session.add(createdEvent)
            db.session.commit()

            return redirect(url_for('calendar'))  # Redirect back to the calendar page

        return render_template('addEvent.html')  # GET method: Display the add event form
    


    @app.route('/viewAllEvents', methods=['GET'])
    def viewAllEvents():
        # Query all events for the logged-in user
        events = Event.query.filter_by(user_id=current_user.id).all()

        return render_template('viewAllEvents.html', events=events)
    




   
    @app.route('/deleteEvent/<int:event_id>', methods=['GET', 'POST'])
    def deleteEvent(event_id):
        # Find the event by its ID
        event = Event.query.get_or_404(event_id)

        if event.user_id != current_user.id:
            flash("You are not authorized to delete this event", category='error')
            return redirect(url_for('calendar'))  # Redirect to the calendar if not the event owner

        if request.method == 'POST':
            # Delete the event from the database
            db.session.delete(event)
            db.session.commit()
            flash("Event deleted successfully", category='success')
            return redirect(url_for('calendar'))  # Redirect to the calendar page

        # GET method: Display confirmation page for event deletion
        return render_template('deleteEvent.html', event=event)



    @app.route('/view_directions/<int:event_id>', methods=['GET', 'POST'])
    def viewRoute(event_id):
        chosenEvent = Event.query.filter_by(id=event_id).first()

        if request.method == 'POST':
            starting_place = request.form['starting_location']
            mode_of_transportation = request.form['mode_of_transportation']

            # Validate starting place
            event_location_check = maps.geocode(starting_place)
            if not event_location_check:
                flash("Place does not exist", category='error')
                return render_template('viewDirections.html', event=chosenEvent)

            # Get ISO format time
            iso_format_time = chosenEvent.start_time.isoformat()

            # Fetch directions
            route = maps.directions(
                starting_place,
                chosenEvent.event_location,
                mode=mode_of_transportation,
                arrival_time=iso_format_time
            )

            if not route:
                flash("No route found.", category='error')
                return redirect(url_for('calendar'))

            return render_template('viewDirections.html', event=chosenEvent, route=route)

        # GET Request - just show form
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
        logout_user()
        return render_template('logout.html')
        

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']

        
            user = User.query.filter_by(username=username).first()
            if user and user.password==password:
                login_user(user)
                return redirect(url_for('calendar'))
            else:
                flash('Wrong username/password',category='error')
        return render_template('loginFINAL.html')