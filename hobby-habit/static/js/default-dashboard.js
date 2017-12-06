"use strict";

$(document).ready(function(){
  // TODO: Create welcome page content for dashboard default view.

  // Show/hide elements based on menu button that was clicked.
  $("#user-profile-menu-btn").click(function (evt) {
    $("#user-profile-content").show();
    $("#my-hobbyhabit-content").hide();
    $("#social > #social-content").hide();
    $("#my-hobbyhabit-content").children().hide();
    $("#dash-welcome").parent().hide();
    $("#my-hobbyhabits-welcome").hide();

    $("#my-hobbyhabits-welcome").parent().hide();
    $("#social-welcome").hide();
  });

  // Show/hide elements based on menu button that was clicked.
  $("#my-hobbyhabits-menu-btn").click(function (evt) {
    $("#user-profile-content").hide();
    $("#my-hobbyhabit-content").show();
    $("#my-hobbyhabit-btns").show();
    $(".page-direction").hide();
    $(".completions-charts").hide();
    $("#social > #social-content").hide();
    $("#hobbyhabit-tracker").hide();
    $("#dash-welcome").parent().hide();

    $("#my-hobbyhabits-welcome").show();
    $("#social-welcome").hide();
  });

  // Show/hide elements based on menu button that was clicked.
  $("#social-menu-btn").click(function (evt) {
    $("#user-profile-content").hide();
    $("#my-hobbyhabit-content").hide();
    $("#my-hobbyhabit-content").children().hide();
    $("#social > #social-content").show();
    $("#dash-welcome").parent().hide();

    $("#my-hobbyhabits-welcome").parent().hide();
    $("#social-welcome").show();
  });

});  // document.ready closer