// Create counting variable.
let numHobbies = 1;

// Attach event listener to element with id plus-btn.
$("#plus-btn").click(function (evt) {

    // Increment numHobbies.
    numHobbies += 1;
    // get the vlaue for the input with the id numHobbies.
    $("#numHobbies").val();  // $("#num-hobbies").val(numHubbies);

    // Create new add hobby field everytime the plus-btn is clicked.
    // let newHobbyNameField = $(`<input type='text' id='hobby-name-${numHobbies}' name='hobby-name-${numHobbies}'>`);  //using string literals to update field with each iteration.
    let newHobbyNameField = $("<input>");

    // Add attributes to the new field.
    newHobbyNameField.attr({"id": "hobby-name-" + numHobbies,
                            "type": "text",
                            "name": "hobby-name-" + numHobbies,
                            "placeholder": "Hobby No." + numHobbies,
    });

    // Put the new input into the DOM.
    $("#add-hobbies").append(newHobbyNameField);

});