"use strict";

// Select element by id and attach event listener to it.
$("#add-hobbyhabit-trigger-btn").click(function (evt) {
  // On click show modal.
  $("#addHobbyHabitModal").modal("show");
});


$.get("/get-hobbies.json", function (results) {
  let hobbies = results;

  $("#add-hobbyhabit-name").autocomplete({
    source: hobbies,
    appendTo : $("#addHobbyHabitModal"),
  });
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
    $("#addHobbyHabitModal").modal("hide");

    // Set html value for success message. Show and fade-out message.
    $("#flash-add-hobbyhabit-status").html("New HobbyHabit successfully added to profile").show().fadeOut(5000);

  // Create html button element and save to variable.
  let newHobbyHabit = $("<div class='col-md-2'><button></button></div>");
  // Add attributes to element.
  newHobbyHabit.attr({"id": "hobbyhabit-btn",
                      "class": "btn btn-info active hobbyhabit-btn",
                      "type": "button",
                      "data-user-hobby-id": results["id"]});

  // Set text value of attribute.
  newHobbyHabit.text(formData["new-hobbyhabit-name"]);
  // Insert button element before element at selected id.
  newHobbyHabit.insertBefore("#add-hobbyhabit-trigger-btn");
  // Create break element and insert before at selected id.
  $("<span>   </span>").insertBefore("#add-hobbyhabit-trigger-btn");

  addHobbyHabitListener();

  // Create html button element and save to variable.
  let newHobbyHabitSoc = $("<button></button>");
  newHobbyHabitSoc.attr({"id": "hobbyhabit-btn",
                      "class": "btn btn-info active social-hobbyhabit-btn",
                      "type": "button",
                      "data-user-hobby-id": results["id"]});

  // Set text value of attribute.
  newHobbyHabitSoc.text(formData["new-hobbyhabit-name"]);

  $("#social-content").append(newHobbyHabitSoc);

  addHobbyHabitListenerSoc();  // Defined in social.js

  });  // add-hobby-dashboard post request function closer
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
    if (completions.length < 5 || startIndex + 5 >= completions.length) {
      $("#next-page-btn").hide();
    }
    else {
      $("#next-page-btn").show();
    }
    if (startIndex > 0) {
      $("#previous-page-btn").show();
    }
    else {
      $("#previous-page-btn").hide();
    }


    // Iterate over slice of completions completion-by-completion.
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

      newCompletions = "<tr id='completion" + completionId + "'>" +
                          "<td>" + completionDate + "</td>" +
                          "<td>" + totalHours + " hr.  " + totalMinutes + " min." + "</td>" +
                          "<td>" + notes + "</td>" +
                          "<td><button class='add-goal-btn btn-info btn-sm edit-btn'>Edit</button><span> </span><button class='add-goal-btn btn-info btn-sm del-btn'>Delete</button></td>" +
                       "</tr>";
// id="add-more" class="add-goal-btn btn-info btn-sm
      // Append value of global variable to element with specified id.
      $("#view-completions").append(newCompletions);
    }  // for loop closer 
}  // viewCompletions function closer


// Declare global variable.
let currentUserhobbyId;

function viewUserHobbyData () {
  startIndex = 0;

  // Create empty object.
  let userData = {};

  // Add property to object.
  userData["user-hobby-id"] = currentUserhobbyId;

  // Show/hide elements at specified ids.
  $("#hobbyhabit-tracker").show();
  $("#view-completions").show();
  $("#user-profile-content").hide();
  $("#my-hobbyhabit-content").show();
  $("#tracker-goal-div").show();
  $("#social > #social-content").hide();
  $("#my-completions").show();

  // AJAX request to send data to route and call specified function.
  $.get("/get-completions.json", userData, viewCompletions);

  // AJAX request to send data to route and call specified function.
  $.get("/get-active-goal.json", userData, viewGoal);

}  // viewUserHobbyData function closer


let userData;

function addHobbyHabitListener () {
  // Select the element by class and attach event listener to it.
  $(".hobbyhabit-btn").click(function (evt) {
    currentUserhobbyId = evt.target.dataset.userHobbyId;
    viewUserHobbyData();
  });
}


let hobbyName;

// Select the element by class and attach event listener to it.
$(".hobbyhabit-btn").click(function (evt) {
  currentUserhobbyId = evt.target.dataset.userHobbyId;
  userData = {'user-hobby-id': currentUserhobbyId};
  // $("#completions-line-chart").show();
  $(".completions-charts").show();

  let lineOptions = {responsive:true};

  let ctxLine = $("#line-chart").get(0).getContext("2d");

  $.get("/get-completions-line-vis.json", userData, function (data) {
    hobbyName = data.hobby_name;
    let lineChart = new Chart(ctxLine, {
      type: 'line',
      data: {
        labels: data.completion_dates,
        datasets: [{
          label: "Tracked Completions",
          fill: true,
          lineTension: 0.5,
          backgroundColor: "rgb(208,89,81)",
          borderCapStyle: 'butt',
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: 'miter',
          pointBorderColor: "rgba(220,220,220,1)",
          pointBackgroundColor: "#fff",
          pointBorderWidth: 0.5,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "rgba(220,220,220,1)",
          pointHoverBorderWidth: 2,
          pointRadius: 3,
          pointHitRadius: 10,
          data: data.total_practice_times,
          spanGaps: false}],
      },
      options: lineOptions
    });
    $("#line-chart-name").html("Completions by Month: " + hobbyName);
  });
});


// Select the element by class and attach event listener to it.
$(".hobbyhabit-btn").click(function (evt) {
  currentUserhobbyId = evt.target.dataset.userHobbyId;
  userData = {'user-hobby-id': currentUserhobbyId};
  $("#completions-bar-chart-grouped").show();

  let barOptions = {responsive: true};

  let ctxBarGrouped = $("#bar-chart-grouped").get(0).getContext("2d");

  $.get("/get-user-hobby-completions-by-year.json", userData, function (data) {
    hobbyName = data.hobby_name;

    let barChartGrouped = new Chart(ctxBarGrouped, {
      type: 'bar',
      data: {
        labels: data.years,
        datasets: [{
          label: 'Total Completions per Year',
          data: data.total_completions_per_year,
          backgroundColor: "rgb(233,181,74)"
        }, {
          label: 'Total Practice Time (Hrs.)',
          data: data.total_hours_per_year,
          backgroundColor: "rgb(69,95,115)"
        }]
      },
        options: barOptions
    });
    $("#bar-chart-grouped-name").html("Total Completions & Practice Time by Year: " + hobbyName);
  });
});


// Select the element by class and attach event listener to it.
$(".hobbyhabit-btn").click(function (evt) {
  // currentUserhobbyId = evt.target.dataset.userHobbyId;
  // userData = {'user-hobby-id': currentUserhobbyId};
  $("#completions-doughnut-chart").show();

  let doughnutOptions = {responsive: true};

  let ctxDoughnut = $("#doughnut-chart").get(0).getContext("2d");

  // $.get("/get-mult-hobbies-vis.json", userData, function (data) {
    $.get("/get-mult-hobbies-vis.json", function (data) {

    let doughnutChart = new Chart(ctxDoughnut, {
      type: 'doughnut',
      tooltipFillColor: "rgba(51, 51, 51, 0.55)",
      data: {
        labels: data.hobby_names,
        datasets: [{
          data: data.completion_count,
          backgroundColor:[
              '#d05951',
              '#1c2947',
              '#aed1c3',
              '#e9b54a',
              '#455f73',
          ],
          borderWidth: 3,
          hoverBackgroundColor: [
              '#de8d87',
              '#31487c',
              '#cbe2d8',
              '#efca80',
              '#7393ab',
              ],
          hoverBorderColor: [],
          hoverBorderWidth: []
        }]
      },
      options: doughnutOptions
    });
  });   
});

  
addHobbyHabitListener();

// Select all elements with specified class and attach event listener to them.
$(".page-direction").click(function (evt){
  // On click, declare variable and set value equal to value of specified data attribute.
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


// Select element by id and attach event listener to it.
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
    $("#user-profile-content").hide();
    $("#my-hobbyhabit-content").show();
    $("#social > #social-content").hide();

    // Set value of html for success message. Show and fade-out message.
    $("#flash-tracking-status").html("HobbyHabit successfully tracked").show().fadeOut(5000);
    // Reset form after submission.
    $("#hobbyhabit-tracker-form")[0].reset();
    
    viewUserHobbyData();
  });  // add-completion post request function closer
});  // hobbyhabit-tracker-btn click closer


// Select element by id and attach datepicker widget to it.
$("#goal-start-date").datepicker();


let viewActiveGoal;
let addGoal;

function viewGoal (results) {  
  $("#view-active-goal").empty();

  let goalData = results;

  if (goalData.active_goal.length !== 0) {
      
    let activeGoal = goalData.active_goal[0];

    let activeGoalId = activeGoal.goal_id;
    let activeGoalStartDate = activeGoal.goal_start_date.slice(0, -13);
    let activeGoalFreqNum = activeGoal.goal_freq_num;
    let activeGoalFreqTimeUnit = activeGoal.goal_freq_time_unit;

    // viewActiveGoal = "<div id='goal" + activeGoalId + "'>" +
    //                     "<b>Goal Start Date</b><p id='goal-start-date'>" + activeGoalStartDate + "</p>" +
    //                     "<b>Goal Frequency</b><p id='goal-freq-num'>" + activeGoalFreqNum + "</p>" +
    //                     "<b>Goal Time Unit</b><p id='goal-freq-time-unit'>" + activeGoalFreqTimeUnit + "</p>" +
    //                  "</div>";   


    viewActiveGoal = "<div id='goal" + activeGoalId + "'>" +
                        "<h3> My Goal</h3>" +
                        "<b>Goal Start Date</b><p id='goal-start-date'>" + activeGoalStartDate + "</p>" +
                        "<b>Goal Frequency</b><p id='goal-freq-num'>" + activeGoalFreqNum + "</p>" +
                        "<b>Goal Time Unit</b><p id='goal-freq-time-unit'>" + activeGoalFreqTimeUnit + "</p>" +
                     "</div>";  

      $("#view-active-goal").append(viewActiveGoal);
      $("#active-goal").show();
      $("#add-goal").hide();
  }
  else if (goalData.active_goal.length === 0) {
    $("#add-goal").show();
    $("#active-goal").hide();
  }

  // NOTE: For data vis.
  // for (let inactiveGoals of goalData.inactive_goals) {

  //     let inactiveGoalId = inactiveGoals.goal_id;
  //     let inactiveGoalStartDate = inactiveGoals.goal_start_date;
  //     let inactiveGoalFreqNum = inactiveGoals.goal_freq_num;
  //     let inactiveGoalFreqTimeUnit = inactiveGoals.goal_freq_time_unit;     
  // }
}


// Select element by id and attach event listener to it.
$("#add-goal-btn").click(function (evt) {
  // On click, prevent form submission.
  evt.preventDefault();
  
  // Create empty object, formData.
  let formData = {};
  // Add properties to object.
  formData["goal-start-date"] = $("#goal-start-date").val();
  formData["goal-freq-num"] = $("#goal-freq-num").val();
  formData["goal-freq-time-unit"] = $("#goal-freq-time-unit").val();
  formData["user-hobby-id"] = currentUserhobbyId;

  // AJAX request to send form data to route and call anonymous function
  // passing in the response/results from request.
  $.post("/add-goal-dashboard", formData, function (results) {
    // Show/hide elements at specified ids.
    $("#user-profile-content").hide();
    $("#my-hobbyhabit-content").show();
    $("#social > #social-content").hide();

    // Set value of html for success message. Show and fade-out message.
    $("#flash-add-goal-status").html("Goal successfully added").show().fadeOut(5000);
    // Reset form after submission.
    $("#add-goal-form")[0].reset();

    viewUserHobbyData();
  });  // add-completion post request function closer
});  // hobbyhabit-tracker-btn click closer


$("#deactivate-goal-btn").click(function (evt) {
  // TODO: Add abilitity to deactivate goal.
  // TODO: Make goal active for "this" goal_id False.
});