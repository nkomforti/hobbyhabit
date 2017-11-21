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

        $("#update-password-btn").click(function (evt) {
        $("#updatePasswordModal").modal("show");
    });

    let lastName = $("#hidden-last-name");
    if ($("#hidden-last-name") !== null) {
        $("#last-name").attr({"value": lastName.val()});
    }
    else {
        $("#last-name").attr({"placeholder": "Last name"});
    }

        $("#update-password-btn").click(function (evt) {
        $("#updatePasswordModal").modal("show");
    });

    let zipcode = $("#hidden-zipcode");
    if ($("#hidden-zipcode") !== null) {
        $("#zipcode").attr({"value": zipcode.val()});
    }
    else {
        $("#zipcode").attr({"placeholder": "Zipcode"});
    }

        $("#update-password-btn").click(function (evt) {
        $("#updatePasswordModal").modal("show");
    });

    let phoneNumber = $("#hidden-phone-number");
    if ($("#hidden-phone-number") !== null) {
        $("#phone-number").attr({"value": phoneNumber.val()});
    }
    else {
        $("#phone-number").attr({"placeholder": "First name"});
    }


    $("#update-profile").click(function (evt) {
        let formData = {};

        formData["first-name"] = $("#first-name").val();
        formData["last-name"] = $("#last-name").val();
        formData.zipcode = $("#zipcode").val();
        formData["phone-number"] = $("#phone-number").val();
        formData["txt-opt-in-out"] = $(".txt-reminder").val();
            
        $.post("/dashboard", formData, function (results) {
            window.location = "/dashboard";
        });
    });

});
