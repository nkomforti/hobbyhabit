"use strict";

$(document).ready(function(){
    $("#user-profile > p").hide();
    $("#my-hobbyhabits > #my-hobbyhabit-content").show();
    $("#social > p").hide();
    $("#settings > p").hide();

    $("#user-profile-menu-btn").click(function(evt) {
        $("#user-profile > p").show();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > p").hide();
        $("#settings > p").hide();
    });

    $("#my-hobbyhabits-menu-btn").click(function(evt) {
        $("#user-profile > p").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").show();
        $("#social > p").hide();
        $("#settings > p").hide();
    });

    $("#social-menu-btn").click(function(evt) {
        $("#user-profile > p").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > p").show();
        $("#settings > p").hide();
    });

    $("#settings-menu-btn").click(function(evt) {
        $("#user-profile > p").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > p").hide();
        $("#settings > p").show();
    });

});