"use strict";

$(document).ready(function(){
  // TODO: Create welcome page content for dashboard default view.

//   function slideDashGif () {

//     // $("#dash-gif").show("slide", { direction: "right" }, 6000);
//     $("#gif").hide("slide", { direction: "right", distance: 250 }, 7000);
//     $("#gif").show("slide", { direction: "left", distance: 250 }, 7000);
    
//   }
// slideDashGif();

//   setInterval(slideDashGif, 8000);

  // Show/hide elements based on menu button that was clicked.
  $("#user-profile-menu-btn").click(function (evt) {
    $("#user-profile > #user-profile-content").show();
    $("#my-hobbyhabit-content").hide();
    $("#social > #social-content").hide();
    $("#my-hobbyhabit-content").children().hide();
    $("#dash-gif").parent().hide();
  });

  // Show/hide elements based on menu button that was clicked.
  $("#my-hobbyhabits-menu-btn").click(function (evt) {
    $("#user-profile > #user-profile-content").hide();
    $("#my-hobbyhabit-content").show();
    $("#my-hobbyhabit-btns").show();
    $(".page-direction").hide();
    $(".completions-charts").hide();
    $("#social > #social-content").hide();
    $("#hobbyhabit-tracker").hide();
    $("#dash-gif").parent().hide();
  });

  // Show/hide elements based on menu button that was clicked.
  $("#social-menu-btn").click(function (evt) {
    $("#user-profile > #user-profile-content").hide();
    $("#my-hobbyhabit-content").hide();
    $("#my-hobbyhabit-content").children().hide();
    $("#social > #social-content").show();
    $("#dash-gif").parent().hide();
  });

});  // document.ready closer