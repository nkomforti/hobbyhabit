"use strict";

// Select element with id goal-start-date and attach datepicker to it.
$("#goal-start-date").datepicker();

// Select elements with class add-goal-btn and attatch event listener to them.
$(".add-goal-btn").click(function (evt) {
    // On click, get value of data attribute for that clicked element ('this')
    // and bind to variable.
    let next = $(this).data("next");

    // Create empty object, formData.
    let formData = {};
    // Add properties to object--the value of each property is the value of the
    // specified selected element id.
    formData["goal-start-date"] = $("#goal-start-date").val();
    formData["goal-freq-num"] = $("#goal-freq-num").val();
    formData["goal-freq-time-unit"] = $("#goal-freq-time-unit").val();
    formData["hobby-id"] = $("#hobby-id").val();

    // AJAX post request to add-goal route to retrieve values from form. Then,
    // depending on which button was clicked, either hide modal for user to
    // select another hobbyhabit, or redirect to dashboard route.
    $.post("/add-goal", formData, function (results) {
        if (next === "add-more") {
            $("#goalModal").modal("hide");
        }
        else {
            window.location = "/dashboard";
        }
    });
});

// Select the element with class hobby-goal-btn and attach event listern to it.
$(".hobby-goal-btn").click(function (evt) {
    // On click, get value of the attribute for that clicked element ('this')
    // and bind to variable.
    let hobbyId = $(this).data("hobbyId");

    // Set the value for the selected element with id hobby-id.
    $("#hobby-id").val(hobbyId);
    // And, create and show modal with id goalModal.
    $("#goalModal").modal("show");

    let hobbyName = $(this).text();
    $("#hobby-name").text(hobbyName);
});