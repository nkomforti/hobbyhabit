"use strict";

let currentUserHobbyId;

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

            // TO DO: Extract data you want to display to user.
                // events = results.events
                // e = events[0]
                // e.name.text
                // e.name.description.text
                // e.url
                // e.start.local, e.start.timezone
                // e.end.local, e.end.timezone
            $("#events").empty();
            
            for (i in events) {
                eventInfo += "<h2>" + events[i].name.text + "</h2>" + "<br>" +
                             "<p>" + events[i].url + "</p>" + "<br>" +
                             "<p>" + events[i].start.local + "</p>" + "<br>" +
                             "<p>" + events[i].start.timezone + "</p>" + "<br><br>";

                // eventInfo += "<h2>" + events[i].name.text + "</h2>" + "<br>";
                // eventInfo += "<p>" + events[i].url + "</p>" + "<br>";
                // eventInfo += "<p>" + events[i].start.local + "</p>" + "<br>";
                // eventInfo += "<p>" + events[i].start.timezone + "</p>" + "<br>";
            }

            $("#events").append(eventInfo);
        }
    });
});