from datetime import datetime
class Calendar:
    
    def __init__(self):
        self.events=[]

    def add_events(self):
        event={}
    
        #PLACEHOLDERS (WILL BE REPLACED BY HTML SYSTEM SOON)
        event_title=input("Enter the event you'd like to enter into the calander: ")
        event_date=input("Enter the date of the event (YYYY-MM-DD HH:MM): ")
        user_datetime = datetime.strptime(event_date, "%Y-%m-%d %H:%M")
        event_description=input("Enter a light description of the event: ")
        event_location=input("Enter the location of the event: ")

        #Adding events to a list of dictionaries
        event["Title"]=event_title
        event["Date"]=user_datetime
        event["Description"]=event_description
        event["Location"]=event_location
        self.events.append(event)
        

        #Sorting the list of the dictionaries to make sure all the dates are in order
        number_of_events=len(self.events)

        for x in range(number_of_events):
            min_index = x
            for j in range(x + 1, number_of_events):
                if self.events[j]["Date"] < self.events[min_index]["Date"]:
                    min_index = j
            self.events[x], self.events[min_index] = self.events[min_index], self.events[x]
    

    #VIEW EVENTS
    def view_events(self):
        if not self.events:
            print("No events scheduled.")
            return

        print("\nScheduled Events:")
        for event in self.events:
            print(f"{event['Date'].strftime('%Y-%m-%d %H:%M')} - {event['Title']}: {event['Description']}")
    


    def delete_events(self):
        deleted_day_events=[]
        find_event_day=input("Enter the day of the event you would like to delete in YYYY-MM-DD format: ")
        delete_day= datetime.strptime(find_event_day, "%Y-%m-%d")
        
        for event in self.events:
            if event["Date"].day==delete_day:
                deleted_day_events.append(event)
        
        for day in deleted_day_events:
            print(f"{day['Date'].strftime('%Y-%m-%d %H:%M')} - {day['Title']}: {day['Description']}")
        

        delete_title=input("Enter the title of the event you would like to delete: ")

        for event in deleted_day_events:
            if event["Title"]==delete_title:
                event_to_delete=event
        self.events.remove(event)



     

        

        

            

c=Calendar()
c.add_events()
c.add_events()
c.view_events()






    