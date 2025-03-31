const calendar = document.querySelector(".calendar"),
  date = document.querySelector(".date");
  daysContainer = document.querySelector(".days");
  prev = document.querySelector(".prev");
  next = document.querySelector(".next"),
  todayBtn  = document.querySelector(".today-btn"),
  gotoBtn  = document.querySelector(".goto-btn"),
  dateInput = document.querySelector(".date-input"),
  eventDate = document.querySelector(".event-date"),
  eventsContainer  = document.querySelector(".events");
  viewSelect = document.querySelector(".select-view");

  viewSelect.addEventListener("change", function () {
    if (this.value === "week") {
        calendar.classList.add("week-view");
    } else {
        calendar.classList.remove("week-view");
    }
  });
 

let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear();
let isWeekView = false;

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



;
viewSelect.addEventListener("change", (e) => {
  isWeekView = e.target.value === "week";
  initCalendar();
});


  //adding days
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
  
  
      let days = "";
  
  
      if (isWeekView) {
        const firstDayOfWeek = new Date(today);
        firstDayOfWeek.setDate(today.getDate() - today.getDay()); // Get Sunday of the week
        
        const startOfWeek = new Date(firstDayOfWeek);
        const endOfWeek = new Date(firstDayOfWeek);
        endOfWeek.setDate(firstDayOfWeek.getDate() + 6); // Saturday of the current week
        date.innerHTML = `${months[startOfWeek.getMonth()]} ${startOfWeek.getDate()} - ${months[endOfWeek.getMonth()]} ${endOfWeek.getDate()} ${year}`;
  
        for (let i = 0; i < 7; i++) {
          let currentDate = new Date(firstDayOfWeek);
          currentDate.setDate(firstDayOfWeek.getDate() + i);
          let dayNum = currentDate.getDate();
          let event = eventsArr.some(e => e.day == dayNum && e.month == month + 1 && e.year == year);
  
          let classes = "day";
          if (event) classes += " event";
          if (
              dayNum == today.getDate() &&
              year == today.getFullYear() &&
              month == today.getMonth()
          ) {
              activeDay = dayNum;
              getActiveDay(dayNum);
              updateEvents(dayNum);
              classes += " today active";
          }
  
          days += `<div class="${classes}">${dayNum}</div>`;
  
          
        }
      }
  
      else{
        date.innerHTML = months[month] + " " + year;
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
    
      }
      
      daysContainer.innerHTML = days;
      addListner();
  
    }

  initCalendar();

  function prevMonth(){
    if (isWeekView) {
      today.setDate(today.getDate() - 7);
    } else {
      month--;
      if (month < 0) {
        month = 11;
        year--;
      }
    }
    initCalendar();
  }

  function nextMonth(){
    if (isWeekView) {
      today.setDate(today.getDate() + 7);
    } else {
      month++;
      if (month > 11) {
        month = 0;
        year++;
      }
    }
    initCalendar();
  }


  prev.addEventListener("click", prevMonth);
  next.addEventListener("click", nextMonth);

  todayBtn.addEventListener("click", () => {
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





  



;


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
            <a href="/deleteEvent/${event.id}" class="delete-event-btn">Delete Event</a>
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
  
  
}

async function fetchEvents() {
  const res = await fetch("/api/events"); // Your Flask route for event data
  const data = await res.json();
  eventsArr = data.events;
  initCalendar();
}

fetchEvents();