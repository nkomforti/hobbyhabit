"use strict";

$("#user-profile-btn").click(function(evt) {
    $("#user-profile").show();
    $("#my-hobbyhabits").hide();
    $("#social").hide();
    $("#settings").hide();
});

$("#my-hobbyhabits-btn").click(function(evt) {
    $("#user-profile").hide();
    $("#my-hobbyhabits").show();
    $("#social").hide();
    $("#settings").hide();
});

$("#social-btn").click(function(evt) {
    $("#my-hobbyhabits").hide();
    $("#user-profile").hide();
    $("#social").show();
    $("#settings").hide();
});

$("#settings-btn").click(function(evt) {
    $("#my-hobbyhabits").hide();
    $("#user-profile").hide();
    $("#social").hide();
    $("#settings").show();
});