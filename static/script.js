
  const calendar = document.querySelector(".calendar"),
    date = document.querySelector(".date"),
    daysContainer = document.querySelector(".days"),
    prev = document.querySelector(".prev"),
    next = document.querySelector(".next"),
    todayBtn  = document.querySelector(".today-btn"),
    gotoBtn  = document.querySelector(".goto-btn"),
    dateInput = document.querySelector(".date-input"),
    eventDate = document.querySelector(".event-date"),
    eventsContainer  = document.querySelector(".events"),
    addEventSubmit = document.querySelector(".add-event-btn");
  
  let today = new Date();
  let activeDay;
  let month = today.getMonth();
  let year = today.getFullYear();
  
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  
  // const eventsArr = [
  //   {
  //     day: 22,
  //     month: 3,
  //     year: 2025,
  //     events: [
  //       {
  //         title: "Event 1",
  //         time: "10:00 AM", 
  //         description: "hihisdfsd",
  //         location: "UA",
  //       },
  //       {
  //         title: "Event w",
  //         time: "11:00 AM", 
  //         description: "asdasdasd",
  //         location: "UA",
  //       },
  //     ],
  //   },
  //   {
  //     day: 14,
  //     month: 3,
  //     year: 2025,
  //     events: [
  //       {
  //         title: "Event 1",
  //         time: "10:00 AM", 
  //         description: "hihisdfsd",
  //         location: "UB",
  //       },
  //     ],
  //   },
  // ];
  
  let eventsArr = [];
  getEvents();
  
    //adding days
    function initCalendar(){
      //get all days of current month and get prev days of last month n and next days of next month
      const firstDay = new Date(year,month, 1);
      const lastDay = new Date(year, month + 1, 0);
      const prevLastDay = new Date (year, month, 0);
      const prevDays = prevLastDay.getDate();
      const lastDate = lastDay.getDate();
      const day = firstDay.getDay();
      const nextDays = 7 - lastDay.getDay() - 1;
  
      date.innerHTML = months[month] + " " + year;
  
      let days = "";
  
      for(let x = day; x > 0; x--){
        days += `<div class = "day prev-day">${prevDays - x + 1}</div>`; 
      }
  
      //current months days
      for(let i=1; i<=lastDate; i++){
  
        //if event is on current day
        let event = false;
        eventsArr.forEach((eventObj) =>{
          if(eventObj.day == i && eventObj.month == month + 1 && eventObj.year == year){
            event = true;
          }
        })
  
        if(i == new Date().getDate() && year == new Date().getFullYear() && month == new Date().getMonth()){ 
  
          activeDay = i;
          getActiveDay(i);
          updateEvents(i);
  
          if(event){
            days += `<div class = "day today active event">${i}</div>`; 
          }
          else{
            days += `<div class = "day today active">${i}</div>`; 
          }
        }
        else{
          if(event){
            days += `<div class = "day event">${i}</div>`; 
          }
          else{
            days += `<div class = "day">${i}</div>`; 
          }
        }
      }
  
      //next month's days
      for(let n=1; n<=nextDays; n++){
        days += `<div class = "day next-day">${n}</div>`
      }
  
      daysContainer.innerHTML = days;
      addListner();
  
    }
  
    initCalendar();
  
    function prevMonth(){
      month--;
      if(month < 0){
        month = 11;
        year--;
      }
      initCalendar();
    }
  
    function nextMonth(){
      month++;
      if(month>11){
        month = 0;
        year++;
      }
      initCalendar();
    }
  
  

    if (todayBtn) todayBtn.addEventListener("click", () => {
    today = new Date();
    month = today.getMonth();
    year = today.getFullYear();
    initCalendar();
  });

    dateInput.addEventListener("input", (e) => {
      let value = dateInput.value.replace(/[^0-9]/g, ""); 
      
      if (value.length >=2) {
        value = value.slice(0, 2) + "/" + value.slice(2, 6);
      }
      dateInput.value = value; 
      if(dateInput.value.length>7){
        dateInput.value = dateInput.value.slice(0,7);
      }
  
      //lets user clear the date they entered incase they entered wrong, without this, only allows user to backspace til the slash
      if(e.inputType == "deleteContentBackward"){
        if(dateInput.value.length == 3){
          dateInput.value = dateInput.value.slice(0,2);
        }
      }
  
    });
  
    gotoBtn.addEventListener("click", gotoDate);
  
    //go to entered date
    function gotoDate(){
      const dateArr = dateInput.value.split("/");
      if(dateArr.length==2){
        if(dateArr[0] > 0 && dateArr[0]<13 && dateArr[1].length == 4){
          month = dateArr[0] - 1;
          year = dateArr[1];
          initCalendar();
          return;
        }
        //if user enters invalid date
        alert("Invalid date");
      }
    }
  
  const addEventBtn = document.querySelector(".add-event"),
    addEventContainer = document.querySelector(".add-event-wrapper"),
    addEventCloseBtn = document.querySelector(".close");
    addEventTitle = document.querySelector(".event-name");
    addEventFrom = document.querySelector(".event-time-from");
    addEventTo = document.querySelector(".event-time-to");
    addEventDescript = document.querySelector(".event-description");
    addEventLocation = document.querySelector(".event-location");
  
  addEventBtn.addEventListener("click", () => {
    addEventContainer.classList.toggle("active");
  })
  
  addEventCloseBtn.addEventListener("click", () => {
    addEventContainer.classList.remove("active");
  })
    
  
  addEventFrom.addEventListener("input", (e) =>{
    //removes anything thats not a number, might not keep this in
    addEventFrom.value = addEventFrom.value.replace(/[^0-9:]/g,"");
    if(addEventFrom.value.length ==2){
      addEventFrom.value += ":";
    }
    //doesnt let user enter more than 5 chars
    if(addEventFrom.value.length >5 ){
      addEventFrom.value = addEventFrom.value.slice(0,5);
    }
  });
  
  addEventTo.addEventListener("input", (e) =>{
    //removes anything thats not a number, might not keep this in
    addEventTo.value = addEventTo.value.replace(/[^0-9:]/g,"");
    if(addEventTo.value.length ==2){
      addEventTo.value += ":";
    }
    //doesnt let user enter more than 5 chars
    if(addEventTo.value.length >5 ){
      addEventTo.value = addEventTo.value.slice(0,5);
    }
  });
  
  
  //function to select days (make them active)
  function addListner() {
    const days = document.querySelectorAll(".day:not(.prev-day):not(.next-day)");
  
    days.forEach((day) => {
      day.addEventListener("click", (e) => {
        //set selected date as active day
        activeDay = Number(e.target.innerHTML);
        
  
        getActiveDay(e.target.innerHTML);
        updateEvents(Number(e.target.innerHTML));
  
        // Remove active class from all days
        days.forEach((day) => day.classList.remove("active"));
  
        // Add active class to the clicked day
        e.target.classList.add("active");
      });
    });
  }
  
  //showing the full date of selected date
  function getActiveDay(date){
    const day = new Date(year, month, date);
    eventDate.innerHTML = months[month] + " " + date + " " + year;
  }
  
  //showing events function
  function updateEvents(date) {
    let events = "";
    eventsArr.forEach((event) => {
      if (
        date == event.day &&
        month + 1 == event.month &&
        year == event.year
      ) {
        event.events.forEach((event) => {
          events += `
          <div class="event">
              <div class="title">
                <i class="fas fa-circle"></i>
                <h3 class="event-title">${event.title}</h3>
              </div>
              <div class="event-time">
                <span class="event-time">${event.time}</span>
              </div>
              <div class="event-description">
                <div class="event-description">${event.description}</div>
              </div>
              <div class="event-location">
                <div class="event-location">${event.location}</div>
              </div>
              <button class="delete-event-btn">Delete Event</button>
          </div>
          `;
        });
      }
    });
    
    if (events === "") {
      events = `<div class="no-event">
              <h3>No Events</h3>
          </div>`;
    }
    eventsContainer.innerHTML = events;
    saveEvents();
    
  }
  
  //function to add events
  addEventSubmit.addEventListener("click", () =>{
    const eventTitle = addEventTitle.value;
    const eventTimeFrom = addEventFrom.value;
    const eventTimeTo = addEventTo.value;
    const eventDescription = addEventDescript.value;  // Get the description input
    const eventLocation = addEventLocation.value;
  
    const timeFrom = convertTime(eventTimeFrom);
    const timeTo = convertTime(eventTimeTo);
  
    const newEvent = {
      title : eventTitle,
      time: timeFrom + " - " + timeTo,
      description: eventDescription,
      location: eventLocation,
    };
  
    let eventAdded = false;
  
    if(eventsArr.length > 0){
      //check if the selected date already has an event 
      eventsArr.forEach((item) => {
        if(item.day == activeDay && item.month == month + 1 && item.year == year){
          item.events.push(newEvent);
          eventAdded = true;
        }
      });
    }
  
    //if selected day has no events or array is empty
    if(!eventAdded){
      eventsArr.push({
        day:activeDay,
        month : month + 1,
        year : year,
        events : [newEvent]
      });
    }
  
    //remove active from add event form
    addEventContainer.classList.remove("active")
  
    //clear fields
    addEventTitle.value = "";
    addEventFrom.value = "";
    addEventTo.value = "";
    addEventDescript.value = "";
    addEventLocation.value = "";
  
    //display added event
    updateEvents(activeDay);
  
    //add event class to new event 
    const activeDayElem = document.querySelector(".day.active");
    //checks to makes sure it does not already have event class
    if(!activeDayElem.classList.contains("event")){
      activeDayElem.classList.add("event");
    }
  
  });
  
  function convertTime(time){
    if (!time || !time.includes(":")) return "Invalid Time";
    let timeArr = time.split(":");
    let timeHour = timeArr[0];
    let timeMin = timeArr[1];
    let timeFormat = timeHour >= 12 ? "PM" : "AM";
    timeHour = timeHour % 12 || 12;
    time = timeHour + ":" + timeMin + " " + timeFormat;
    return time;
  }
  
  //deleting events
  eventsContainer.addEventListener("click", (e) => {
    if(e.target.classList.contains("delete-event-btn")){
      const eventTitle = e.target.closest('.event').querySelector('.event-title').innerHTML;
      eventsArr.forEach((event) => {
        if(event.day == activeDay && event.month == month + 1 && event.year == year){
          event.events.forEach((item, index) => {
            if(item.title == eventTitle){
              event.events.splice(index, 1);
            }
          });
  
          //remove day from events if no events left
          if(event.events.length==0){
            eventsArr.splice(eventsArr.indexOf(event), 1);
            const activeDayElem = document.querySelector(".day.active");
            if(activeDayElem.classList.contains("event")){
              activeDayElem.classList.remove("event");
            }
          }
        }
      });
    
      updateEvents(activeDay);
    }
  });
  
  
  //saving to local storage 
  function saveEvents(){
    console.log("yes");
    localStorage.setItem("events", JSON.stringify(eventsArr));
  }
  
  function getEvents(){
    if(localStorage.getItem("events") === null){
      return;
    }
    eventsArr = JSON.parse(localStorage.getItem("events"));
  }
  
  
 