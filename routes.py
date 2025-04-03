from flask import Flask, render_template,request,redirect,url_for,flash,session,jsonify,Response
from datetime import datetime, timedelta
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
                "location": event.event_location,
                "description":event.event_description
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
            description=request.form['description']

            try:
                starting_time = datetime.strptime(event_start, '%Y-%m-%dT%H:%M')
                ending_time = datetime.strptime(event_end, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash("Invalid date format. Please use the correct format.", category='error')
                return render_template('addEvent.html')
            
            if len(event_name)>=100:
                flash("Title must be less then 100 characters",catagory='error')
                return render_template('addEvent.html')
            
            if len(location)>=200:
                flash("Location must be less then 200 characters",catagory='error')
                return render_template('addEvent.html')

            if starting_time >= ending_time:
                flash("Event start time cannot be after the end time", category='error')
                return render_template('addEvent.html')
            
            if not event_name or not event_name.strip():
                flash("Event Name Cannot Be Empty", category='error')
                return render_template('addEvent.html')
            
            if not event_name.strip():
                flash("Description can't be empty spaces", category='error')
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
                event_description=description,
                user_id=current_user.id
                
            )
            db.session.add(createdEvent)
            db.session.commit()

            return redirect(url_for('calendar'))  # Redirect back to the calendar page

        return render_template('addEvent.html')  # GET method: Display the add event form
    


    
   
    @app.route('/deleteEvent/<int:event_id>', methods=['GET', 'POST'])
    def deleteEvent(event_id):
        # Find the event by its ID
        event = Event.query.filter_by(id=event_id).first()

        if request.method == 'POST':
            # Delete the event from the database
            selection=request.form['confirm']
            if selection=="yes":
                db.session.delete(event)
                db.session.commit()
                return redirect(url_for('calendar'))  # Redirect to the calendar page
            else:
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
            iso_format_time = chosenEvent.event_start.isoformat()

            # Fetch directions
            route = maps.directions(
                starting_place,
                chosenEvent.event_location,
                mode=mode_of_transportation,
                arrival_time=iso_format_time
            )

            if not route:
                flash("No route found.", category='error')
                return render_template('viewDirections.html', event=chosenEvent)
            
            duration_seconds = route[0]['legs'][0]['duration']['value']
            travel_time = timedelta(seconds=duration_seconds)
            time_to_leave=chosenEvent.event_start-travel_time

            return render_template('viewRoute.html', event=chosenEvent, route=route, starting_place=starting_place, mode_of_transportation=mode_of_transportation, travel_time=travel_time, time_to_leave=time_to_leave)

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
            
            if len(password)<8:
                flash('Password has to be at least 8 characters', category='error')
        
            if not existing_user and confirm_password==password and len(password)>=8:
                new_user = User(username=username, password=password)  
                db.session.add(new_user)
                db.session.commit()
                return redirect (url_for('login')) 
        return render_template('register.html')
        


    @app.route('/logout', methods=['POST'])
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
    
    @app.route('/downloadEvents', methods=['GET','POST'])
    def download():
        if request.method=="POST":
            events = Event.query.filter_by(user_id=current_user.id).all()
            startingtime_string=request.form.get('starting_time')
            endingtime_string=request.form.get('end_time')

            if startingtime_string>endingtime_string:
                flash ("Start time can't be greater then end time", catatory="error")
                return render_template('download.html')

            starting_time = datetime.strptime(startingtime_string, '%Y-%m-%dT%H:%M')
            ending_time = datetime.strptime(endingtime_string, '%Y-%m-%dT%H:%M')

            existing_event=False
            event_in_timeframe=[]
            for event in events:
                if event.event_start>=starting_time and event.event_end<=ending_time:
                    existing_event=True
                    event_in_timeframe.append(event)
            
            file_content=f"EVENT INFORMATION FROM {starting_time.strftime('%Y-%m-%d %H:%M')}- {ending_time.strftime('%Y-%m-%d %H:%M')}\n\n"
            if existing_event==True:
                for event in event_in_timeframe:
                    file_content+=f"Event Name:{event.event_title}\nEvent Location:{event.event_location}\nEvent Start:{event.event_start}\nEvent End:{event.event_end}\n"
                    if event.event_description:
                        file_content+=f"Description:{event.event_description}\n\n"
                    else:
                        file_content+="\n\n"
            
            else:
                file_content+="NO EVENTS IN SELECTED TIMEFRAME"
            
            response = Response(file_content, mimetype="text/plain")
            response.headers.set("Content-Disposition", "attachment", filename="events.txt")
            return response
        return render_template('download.html')
            




