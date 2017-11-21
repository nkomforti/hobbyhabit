"use strict";

$(document).ready(function(){
    $("#user-profile > #user-profile-content").hide();
    $("#my-hobbyhabits > #my-hobbyhabit-content").show();
    $("#social > #social-content").hide();
    $("#settings > #settings-content").hide();

    $("#user-profile-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").show();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").hide();
        $("#settings > #settings-content").hide();
    });

    $("#my-hobbyhabits-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").show();
        $("#social > #social-content").hide();
        $("#settings > #settings-content").hide();
    });

    $("#social-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").show();
        $("#settings > #settings-content").hide();
    });

    $("#settings-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").hide();
        $("#settings > #settings-content").show();
    });

    $("#update-password-btn").click(function (evt) {
        $("#updatePasswordModal").modal("show");
    });

    let firstName = $("#hidden-first-name");
    if ($("#hidden-first-name") !== null) {
        $("#first-name").attr({"value": firstName.val()});
    }
    else {
        $("#first-name").attr({"placeholder": "First name"});
    }

});
