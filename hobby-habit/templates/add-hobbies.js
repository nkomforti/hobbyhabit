let numHobbies = 1;

$("#plus-btn").click(function (evt) {

    //increment numHobbies
    numHobbies += 1;
    $("#num-hobbies").val(numHubbies);

    //create new field
    let newHobbyNameField = $("<input>");  //does this need the input name or id??
    //add attributes
    newHobbyNameField.attr({"id": "hobby-name-" + numHobbies,
    "type": "text",
    "name": "hobby-name-" + numHobbies,
    "placeholder": "Hobby No." + numHobbies,
    });

    //put new input into the DOM
    $("#add-hobbies").append(newHobbyNameField);

});