"use strict";

$(document).ready(function(){
    // Default dashboard view.  // CREATE WELCOME CONTENT/MESSAGE
    $("#user-profile > #user-profile-content").hide();
    $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
    $("#social > #social-content").hide();
    $("#hobbyhabit-tracker").hide();
    $("#view-completions").hide();
    $(".page-direction").hide();

    // Show/hide elements based on menu button that was clicked.
    $("#user-profile-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").show();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").hide();
    });

    // Show/hide elements based on menu button that was clicked.
    $("#my-hobbyhabits-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").show();
        $("#social > #social-content").hide();
        $("#hobbyhabit-tracker").hide();
    });

    // Show/hide elements based on menu button that was clicked.
    $("#social-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").show();
    });

});  // document.ready closer