"use strict";

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

  // Add properties to object from profile form--the value of each property is
  // the value of the specified selected element id.
  formData["first-name"] = $("#first-name").val();
  formData["last-name"] = $("#last-name").val();
  formData.zipcode = $("#zipcode").val();
  formData["phone-number"] = $("#phone-number").val();
  formData["txt-opt-in-out"] = $(".txt-reminder").val();
  
  // AJAX request to send form data to route and call anonymous function passing
  // in the response/results from request.
  $.post("/update-profile", formData, function (results) {
    $("#user-profile > #user-profile-content").show();
    $("#my-hobbyhabits > #my-hobbyhabit-content").hide();
    $("#social > #social-content").hide();

    // Set html value for success message.
    $('#flash-update-profile-status').html("Successfully saved changes to profile").show().fadeOut(5000);
  });
});  // update-profile click closer