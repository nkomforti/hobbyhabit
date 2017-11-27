"use strict";

$(document).ready(function(){
    // Set default dashboard view to see My HobbyHabit overview page (not hobbyhabit specific).
    $("#user-profile > #user-profile-content").hide();
    $("#my-hobbyhabits > #my-hobbyhabit-content").show();
    $("#social > #social-content").hide();
    $("#settings > #settings-content").hide();
    $("#hobbyhabit-tracker").hide();
    $("#view-completions").hide();

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
        $("#hobbyhabit-tracker").hide();
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

    let firstName = $("#hidden-first-name");
    if ($("#hidden-first-name") !== null) {
        $("#first-name").attr({"value": firstName.val()});
    }
    else {
        $("#first-name").attr({"placeholder": "First name"});
    }

    let lastName = $("#hidden-last-name");
    if ($("#hidden-last-name") !== null) {
        $("#last-name").attr({"value": lastName.val()});
    }
    else {
        $("#last-name").attr({"placeholder": "Last name"});
    }

    let zipcode = $("#hidden-zipcode");
    if ($("#hidden-zipcode") !== null) {
        $("#zipcode").attr({"value": zipcode.val()});
    }
    else {
        $("#zipcode").attr({"placeholder": "Zipcode"});
    }

    $("#update-password-trigger-btn").click(function (evt) {
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
            
        $.post("/update-user-profile", formData, function (results) {
            $("#user-profile > #user-profile-content").show();
            $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
            $("#social > #social-content").hide();
            $("#settings > #settings-content").hide();

            $('#flash-update-profile-status').html("Successfully saved changes to profile").show().fadeOut(5000);
        });
    });

    let currentUserhobbyId;

    $("#add-hobbyhabit-trigger-btn").click(function (evt) {
        $("#addHobbyhabitModal").modal("show"); //STILL NEED TO ADD AND COMMIT TO DB
    });

    $("#add-hobbyhabit-btn").click(function (evt) {
        let formData = {};

        formData["new-hobbyhabit-name"] = $("#add-hobbyhabit-name").val();

        $.post("/add-hobby-dashboard", formData, function (results) {
            $("#addHobbyhabitModal").modal("hide"); //NOT WORKING
            $("#flash-add-hobbyhabit-status").html("New HobbyHabit successfully added to profile").show().fadeOut(5000);
        });
    });

    // Create global variable.
    let newComletions;

    // Select the element with class hobbyhabit-btn and attach event listener to it.
    $(".hobbyhabit-btn").click(function (evt) {
        currentUserhobbyId = $(this).data("userHobbyId");

        let userData = {};

        userData["user-hobby-id"] = currentUserhobbyId;

        $("#hobbyhabit-tracker").show();
        $("#view-completions").show();

        function viewCompletions (results) {
            console.log(results);  // For debugging.

            // Clear/reset div element with the id view-completions each time a
            // different hobbyhabit is clicked.
            $("#view-completions").html("");

            for (let i in results) {
                let completionId = (results[i].completion_id);
                let completionDate = (results[i].completion_date).slice(0, -13);
                let totalPracticeTime = (results[i].total_practice_time);
                let totalHours = Math.floor(totalPracticeTime / 60);          
                let totalMinutes = totalPracticeTime % 60;
                let notes;

                if ((results[i].notes) === null) {
                    notes = "<i>This completion was tracked without a note.</i>";
                }
                else{
                    notes = (results[i].notes);
                }

                newComletions = "<div id='" + completionId + "' class='userhobby-completion'" + ">" +
                                    "<b>Completion Date</b><p id='completion-date'>" + completionDate + "</p>" +
                                    "<b>Total Hours</b><p id='total-hours'>" + totalHours + "</p>" +
                                    "<b>Total Minutes</b><p id='total-minutes'>" + totalMinutes + "</p>" +
                                    "<b>Notes</b><p id='notes'>" + notes + "</p>" + 
                                "</div>";

                $("#view-completions").append(newComletions);
            }
        }
            $("#user-profile > #user-profile-content").hide();
            $("#my-hobbyhabits > #my-hobbyhabit-content").show();
            $("#social > #social-content").hide();
            $("#settings > #settings-content").hide();

        $.get("/view-completions.json", userData, viewCompletions);

    });  //.hobbyhabit-btn click closer

    $("#completion-date").datepicker();

    $("#hobbyhabit-tracker-btn").click(function (evt) {
        evt.preventDefault();
        // Create empty object, formData.
        let formData = {};
        // Add properties to object--the value of each property is the value of the
        // specified selected element id.
        formData["completion-date"] = $("#completion-date").val();
        formData["total-hours"] = $("#total-hours").val();
        formData["total-minutes"] = $("#total-minutes").val();
        formData.notes = $("#notes").val();
        formData["user-hobby-id"] = currentUserhobbyId;

        // AJAX post request to add-completion route to retrieve values from form. Then,
        // depending on which button was clicked, either hide modal for user to
        // select another hobbyhabit, or redirect to dashboard route.
        $.post("/add-completion", formData, function (results) {
            $("#user-profile > #user-profile-content").hide();
            $("#my-hobbyhabits > #my-hobbyhabit-content").show();
            $("#social > #social-content").hide();
            $("#settings > #settings-content").hide();

            // Flash success message.
            $("#flash-tracking-status").html("HobbyHabit successfully tracked").show().fadeOut(5000);
            // Reset form after submission.
            $("#hobbyhabit-tracker-form")[0].reset();
        });
    });

});  //closer for document.ready
