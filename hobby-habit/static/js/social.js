"use strict";

let currentUserHobbyId;
function addHobbyHabitListenerSoc () {

$(".social-hobbyhabit-btn").click(function (evt) {
  let userData = {};

  currentUserHobbyId = evt.target.dataset.userHobbyId;

  userData["user-hobby-id"] = currentUserHobbyId;

  $.get("/social.json", userData, function (results) {

    if (results === {}) {
      $("#flash-no-events").html("No related events are scheduled in your area at this time").show().fadeOut(5000);
      // TO DO: Add graphic.
    }
    else if (results === "Does not meet requirements") {
      $("#flash-fail-req").html("Please provide your zipcode to see any related events in your area").show().fadeOut(5000);
      // TO DO: Redirect to user profile page at zipcode
    }
    else {
      let i;
      let eventInfo = "";
      let events = results.events;

      // NOTE: Extract data from results that you want to display to user.
          // events = results.events
          // e = events[0]
          // e.name.text
          // e.name.description.text
          // e.url
          // e.start.local, e.start.timezone
          // e.end.local, e.end.timezone
      $("#events").empty();
      
      let eventsHeading = "<h3>Potential Events</h3>" + "<br>";

      for (i in events) {
        if (events[i].description.text !== null){

          eventInfo += "<ul>" +
                          "<li><a href='" + events[i].url + "'>" + events[i].name.text + "</a></li>" +
                          "<li>" + events[i].description.text.slice(0, 300) + "..." + "</li>" +
                          "<li>" + events[i].start.local.slice(0, -9) + "</li>" +
                       "</ul>" + "<br>";
        }
        else {
          eventInfo += "<ul>" +
                          "<li><a href='" + events[i].url + "'>" + events[i].name.text + "</a></li>" +
                          "<li><i>No description available.</i></li>" +  // TODO: Add check for if event.description.text == null
                          "<li>" + events[i].start.local.slice(0, -9) + "</li>" +
                       "</ul>" + "<br>";
        }
      }

      $("#events").append(eventsHeading);
      $("#events").append(eventInfo);
    }
  });
});
}
addHobbyHabitListenerSoc();