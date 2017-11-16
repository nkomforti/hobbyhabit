"use strict";

// Select element with id plus-button and attach an event listener to it that
// will call the following anonymous function when clicked.
$("#plus-btn").click(function (evt) {

    // Get the vlaue for the input with the id numHobbies and bind to variable.
    let numHobbies = $("#num-hobbies").val();
    // Convert string to integer.
    numHobbies = parseInt(numHobbies);
    // Increment numHobbies.
    numHobbies += 1;

    // Every time the plus button is clicked, create new add hobby input field.
    let newHobbyNameField = $("<input>");
    // Add attributes and values to the new input field.
    newHobbyNameField.attr({"id": "hobby-name-" + numHobbies,
                            "type": "text",
                            "name": "hobby-name-" + numHobbies,
                            "placeholder": "HobbyHabit No. " + numHobbies,
    });

    // Put the new input into the DOM.
    $("<br>").insertBefore("#plus-btn");
    newHobbyNameField.insertBefore("#plus-btn");


    // Get the value for the input witht the id num-hobbies.
    $("#num-hobbies").val(numHobbies);
    // Disable the properties for the element with the id plus-btn.
    $("#plus-btn").prop("disabled", true);
});

// Select entire page/document and attach an event listenter to it that will
// call the following anonymous function when a key on the keyboard is released.
$(document).on("keyup", "#add-hobbies input", function (evt) {

        // Create variable to track input field values; set to false to start.
        let empty = false;

        // Select all elements with the id add-hobbies that are also input
        // elements, and run method to iterate over the collection of elements
        // and will call the following function. 
        $("#add-hobbies input").each(function (evt){

            // Check if the input value of the current loop iteration (object
            // that currently "owns" the function) is equal to an empty string.
            if ($(this).val() === "" ){
                // If value equals empty string, disable plus button, and set
                // tracking variable equal to true (because field is empty).
                $("#plus-btn").prop("disabled", true);
                empty = true;
            }
        });

        // Check if tracking variable equals false (input fields not empty).
        // If false enable plus button.
        if (empty === false) {
            $("#plus-btn").prop("disabled", false);
        }
    });