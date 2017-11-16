"use strict";

// $(function insertDatepicker() {
//     $("#goal-start-date").datepicker();
// });

$("#goal-start-date").click($(function(evt) {
    $( "#goal-start-date" ).datepicker();
} );

$(".add-goal-btn").click(function(evt) {
    let next = $(this).data("next");
    let formData = {};
    formData.goal-start-date = $("#goal-start-date").val();
    formData.goal-freq-num = $("#goal-freq-num").val();
    formData.goal-freq-time-unit = $("#goal-freq-time-unit").val();
    formData.hobby-id = $("#hobby-id").val();

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