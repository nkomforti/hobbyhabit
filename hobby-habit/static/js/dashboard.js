"use strict";

$(document).ready(function(){
    // Set default dashboard view to see My HobbyHabit overview page.
    $("#user-profile > #user-profile-content").hide();
    $("#my-hobbyhabits > #my-hobbyhabit-content").show();
    $("#social > #social-content").hide();
    $("#settings > #settings-content").hide();
    $("#hobbyhabit-tracker").hide();
    $("#view-completions").hide();

    // Show/hide elements based on menu button that was clicked.
    $("#user-profile-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").show();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").hide();
        $("#settings > #settings-content").hide();
    });

    // Show/hide elements based on menu button that was clicked.
    $("#my-hobbyhabits-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").show();
        $("#social > #social-content").hide();
        $("#settings > #settings-content").hide();
        $("#hobbyhabit-tracker").hide();
    });

    // Show/hide elements based on menu button that was clicked.
    $("#social-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").show();
        $("#settings > #settings-content").hide();
    });

    // Show/hide elements based on menu button that was clicked.
    $("#settings-menu-btn").click(function (evt) {
        $("#user-profile > #user-profile-content").hide();
        $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
        $("#social > #social-content").hide();
        $("#settings > #settings-content").show();
    });

    // Select (hidden) element by id and save to variable.
    let firstName = $("#hidden-first-name");
    // Check if value exists.
    // If value not null, select (non-hidden) element and assign value from hidden.  
    if ($("#hidden-first-name") !== null) {
        $("#first-name").attr({"value": firstName.val()});
    }
    // If value is null, assign placeholder.
    else {
        $("#first-name").attr({"placeholder": "First name"});
    }

    // Select (hidden) element by id and save to variable.
    let lastName = $("#hidden-last-name");
    // Check if value exists.
    // If value not null, select (non-hidden) element and assign value from hidden. 
    if ($("#hidden-last-name") !== null) {
        $("#last-name").attr({"value": lastName.val()});
    }
    // If value is null, assign placeholder.
    else {
        $("#last-name").attr({"placeholder": "Last name"});
    }

    // Select (hidden) element by id and save to variable.
    let zipcode = $("#hidden-zipcode");
    if ($("#hidden-zipcode") !== null) {
        $("#zipcode").attr({"value": zipcode.val()});
    }
    // Check if value exists.
    // If value not null, select (non-hidden) element and assign value from hidden.
    else {
        $("#zipcode").attr({"placeholder": "Zipcode"});
    }

    // Select element by id and attach event listener.
    $("#update-password-trigger-btn").click(function (evt) {
        // On click, show modal.
        $("#updatePasswordModal").modal("show");
    });

    // Select (hidden) element by id and save to variable.
    let phoneNumber = $("#hidden-phone-number");
    if ($("#hidden-phone-number") !== null) {
        $("#phone-number").attr({"value": phoneNumber.val()});
    }
    // Check if value exists.
    // If value not null, select (non-hidden) element and assign value from hidden.
    else {
        $("#phone-number").attr({"placeholder": "Phone number"});
    }

    // Select element by id and attach event listener.
    $("#update-profile").click(function (evt) {
        // Create empty object.
        let formData = {};

        // Add properties to object from profile form--the value of each
        // property is the value of the specified selected element id..
        formData["first-name"] = $("#first-name").val();
        formData["last-name"] = $("#last-name").val();
        formData.zipcode = $("#zipcode").val();
        formData["phone-number"] = $("#phone-number").val();
        formData["txt-opt-in-out"] = $(".txt-reminder").val();
        
        // AJAX request to send form data to route and call anonymous function
        // to show/hide elements elements and flash success message and get
        // request response/results containing data from database.
        $.post("/update-user-profile", formData, function (results) {
            $("#user-profile > #user-profile-content").show();
            $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
            $("#social > #social-content").hide();
            $("#settings > #settings-content").hide();

            // Set html value for success message.
            $('#flash-update-profile-status').html("Successfully saved changes to profile").show().fadeOut(5000);
        });
    });  // update-profile click closer

    // Declare global variable.
    let currentUserhobbyId;

    // Select element by id and attach event listener to it.
    $("#add-hobbyhabit-trigger-btn").click(function (evt) {
        // On click show modal.
        $("#addHobbyhabitModal").modal("show");
    });

    // Select element by id and attach event listener to it.
    $("#add-hobbyhabit-btn").click(function (evt) {
        // Create empty object.
        let formData = {};

        // Add property to object from add hobbyhabit modal form.
        formData["new-hobbyhabit-name"] = $("#add-hobbyhabit-name").val();

        // AJAX request to send form data to route and call anonymous function
        // passing in the response/results from request.
        $.post("/add-hobby-dashboard", formData, function (results) {
            $("#addHobbyhabitModal").modal("hide");

            // Set html value for success message. Show and fade-out message.
            $("#flash-add-hobbyhabit-status").html("New HobbyHabit successfully added to profile").show().fadeOut(5000);

        });  // add-hobby-dashboard post request function closer

        // Create html button element and save to variable.
        let newHobbyHabit = $("<button></button>");
        // Add attributes to element.
        newHobbyHabit.attr({"id": "hobbyhabit-btn",
                            "class": "btn btn-info active hobbyhabit-btn",
                            "type": "button",
                            "data-user-hobby-id": "{{ user_hobby['user_hobby_id'] }}"});

        // Set text value of attribute.
        newHobbyHabit.text(formData["new-hobbyhabit-name"]);
        // Insert button element before element at selected id.
        newHobbyHabit.insertBefore("#add-hobbyhabit-trigger-btn");
        // Create break element and insert before at selected id.
        $("<br>").insertBefore("#add-hobbyhabit-trigger-btn");

    });  // add-hobbyhabit-btn click closer

    // Declare global variable.
    let newCompletions;
    // Declare global variable.
    let completions;
    // Declare global variable and set value to 0.
    let startIndex = 0;

    // Declare function and pass in results from server response.
    function viewCompletions (results) {
        // Set the value of global variable to results from server response.
        completions = results;

        // Empty element with the id view-completions.
        $("#view-completions").empty();

        // Iterate over slice of completions completion-by-completion; declare
        // variable completion.
        for (let completion of completions.slice(startIndex, startIndex + 5)) {

            // Declare variable and bind result at specified key.
            let completionId = completion.completion_id;
            // Declare variable and bind result slice at specified key.
            let completionDate = (completion.completion_date).slice(0, -13);
            // Declare variable and bind result at specified key.
            let totalPracticeTime = completion.total_practice_time;
            // Declare variable and bind result at specified key divided by 60.
            let totalHours = Math.floor(totalPracticeTime / 60);
            // Declare variable and bind result at specified key by modulo 60.         
            let totalMinutes = totalPracticeTime % 60;
            // Declare variable.
            let notes;

            // Check if result at specified key is null.
            if ((completion.notes) === null) {
                // If null, assign string as value.
                notes = "<i>This completion was tracked without a note.</i>";
            }
            else{
                // Otherwise assign value of result at specified key.
                notes = completion.notes;
            }

            // Set value of global variable to div element and its children.
            newCompletions = "<div id='" + completionId + "' class='userhobby-completion'" + ">" +
                                "<b>Completion Date</b><p id='completion-date'>" + completionDate + "</p>" +
                                "<b>Total Practice Time</b><p id='total-practice-time'>" + totalHours + " hr.  " + totalMinutes + " min." + "</p>" +
                                "<b>Notes</b><p id='notes'>" + notes + "</p>" + 
                            "</div>";

            // Append value of global variable to element with specified id.
            $("#view-completions").append(newCompletions);

        }  // for loop closer 
    }  // viewCompletions function closer

    // Select the element by id and attach event listener to it.
    $(".hobbyhabit-btn").click(function (evt) {
        // On click, declare variable and set value equal to value of specified
        // data attribute.
        currentUserhobbyId = $(this).data("userHobbyId");

        // Create empty object.
        let userData = {};

        // Add property to object.
        userData["user-hobby-id"] = currentUserhobbyId;

        // Show element at specified id.
        $("#hobbyhabit-tracker").show();
        // Show element at specified id.
        $("#view-completions").show();

            // Show/hide elements at specified ids.
            $("#user-profile > #user-profile-content").hide();
            $("#my-hobbyhabits > #my-hobbyhabit-content").show();
            $("#social > #social-content").hide();
            $("#settings > #settings-content").hide();

        // AJAX request to send data to route and call specified function.
        $.get("/view-completions.json", userData, viewCompletions);

    });  // hobbyhabit-btn click closer

    // Select all elements with specified class and attach event listener to them.
    $(".page-direction").click(function (evt){
        // On click, declare variable and set value equal to value of specified
        // data attribute.
        let pageDirection = $(this).data("page-direction");

        // Check if value is equal to specified string.
        if (pageDirection === "next") {
            // If equal, increment value of global variable by 5.
            startIndex += 5;
            // Call specified function and pass in global variable.
            viewCompletions(completions);
        }
        else {
            // If not equal, decrement value of global variable by 5.
            startIndex -= 5;
            // Call specified function and pass in global variable.
            viewCompletions(completions);
        }
    });  // view-direction click closer

    // Select element by id and attach datepicker widget to it.
    $("#completion-date").datepicker();

    // Select element by id and attache event listener to it.
    $("#hobbyhabit-tracker-btn").click(function (evt) {
        // On click, prevent form submission.
        evt.preventDefault();
        // Create empty object, formData.
        let formData = {};

        // Add properties to object.
        formData["completion-date"] = $("#completion-date").val();
        formData["total-hours"] = $("#total-hours").val();
        formData["total-minutes"] = $("#total-minutes").val();
        formData.notes = $("#notes").val();
        formData["user-hobby-id"] = currentUserhobbyId;

        // AJAX request to send form data to route and call anonymous function
        // passing in the response/results from request.
        $.post("/add-completion", formData, function (results) {
            // Show/hide elements at specified ids.
            $("#user-profile > #user-profile-content").hide();
            $("#my-hobbyhabits > #my-hobbyhabit-content").show();
            $("#social > #social-content").hide();
            $("#settings > #settings-content").hide();

            // Set value of html for success message. Show and fade-out message.
            $("#flash-tracking-status").html("HobbyHabit successfully tracked").show().fadeOut(5000);
            // Reset form after submission.
            $("#hobbyhabit-tracker-form")[0].reset();

        });  // add-completion post request function closer
    });  // hobbyhabit-tracker-btn click closer


    // check if any active goal for selected userhobby
    // yes, display goal 
    // no, display add goal form
    // edit goal
    // deactivate goal
    let goalData;
    let viewActiveGoal;
    let addGoal;

    function viewGoal (results) {
        goalData = results;

        for (let goal of goalData) {

            let activeGoalActive = goal.active_goal;
            let activeGoalId = goalData.goal_
            let activeGoalStartDate =
            let activeGoalFreqNum =
            let activeGoalFreqTimeUnit =

            let inactiveGoalActive = goal.inactive_goal;
            let inactiveGoalId = goalData.
            let inactiveGoalStartDate =
            let inactiveGoalFreqNum =
            let inactiveGoalFreqTimeUnit =

            if (goalActive !== []) {
                viewActiveGoal = "<div id='" + activeGoalId + "'>" +
                                    "<b>Goal Start Date</b><p id='goal-start-date'>" + goalStartDate + "</p>" +
                                    "<b>Goal Frequency</b><p id='goal-freq-num'>" + goalFreqNum + "</p>" +
                                    "<b>Goal Time Unit</b><p id='goal-freq-time-unit'>" + goalFreqTimeUnit + "</p>" + 
                                "</div>";

                $("#view-active-goal").append(viewActiveGoal);
                $("#view-active-goal").show();
                $("#add-gaol").hide();
            }
            else {
                addGoal = 
                $("#add-gaol").show();
                $("#view-active-goal").hide();
            }
        }
    }
        // AJAX request to send data to route and call specified function.
        $.get("/view-active-goal.json", userData, viewGoal);





});  // document.ready closer
