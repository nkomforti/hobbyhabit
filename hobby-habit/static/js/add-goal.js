"use strict";

// Select element with id goal-start-date and attach datepicker to it.
$("#goal-start-date").datepicker();

// Select elements with class add-goal-btn and attatch event listener to them.
$(".add-goal-btn").click(function(evt) {
    // On click 
    let next = $(this).data("next");
    let formData = {};
    formData["goal-start-date"] = $("#goal-start-date").val();
    formData["goal-freq-num"] = $("#goal-freq-num").val();
    formData["goal-freq-time-unit"] = $("#goal-freq-time-unit").val();
    formData["hobby-id"] = $("#hobby-id").val();

    $.post("/add-goal", formData, function(results) {
        if (next === "add-more") {
            $("#goalModal").modal("hide");
        }
        else {
            window.location = "/dashboard";
        }
    });
});

$(".hobby-goal-btn").click(function(evt) {
    let hobbyId = $(this).data("hobbyId");
    $("#hobby-id").val(hobbyId);
    $("#goalModal").modal("show");
});