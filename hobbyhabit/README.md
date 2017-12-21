# HobbyHabit
HobbyHabit is a hobby/task tracking application that lets users track their
progress for any activity they want to hold themselves more accountable for.
Users can set goals based on what they want to achieve, schedule text reminders,
find events where they can socialize with others in their area interested in the
same activities, and toggle between several data visualizations that make
analyzing the details of their progress easy and approachable, so that marveling
at their hard work is a snap and they can get back to getting things done! 

## Technologies Used
* Python
* Flask
* PostgresSQL
* HTML
* CSS
* Javascript/jQuery
* AJAX/JSON
* Jinja2
* Chart.js
* Bootstrap
* Eventbrite API
* Twilio API

## How to Run Locally
*HobbyHabit is not deployed.*

* Create a python virtual environment and install all dependencies:

`$ pip install -r requirements.txt`

* Create a database called hobbyhabit:

`$ createdb hobbyhabit`

* Create all tables in the database:

`$ python model.py`

* Start Flask server:

`$ python server.py`

* Access the web app in browser at localhost:5000

## Features and Flow

#### New User:
* Create account on homepage

[Homepage](hobbyhabit/doc/homepage.png)

* New page renders for user to add HobbyHabits to track, this page uses 
javascript/jQuery to dynamically add form-fields for the user to add any number
HobbyHabits to track

* New page renders for user to set optional goals for their HobbyHabits via a
bootstrap modal, or select the option to skip aheat to their dashboard

* New page renders showing user's dashboard

* Additional HobbyHabits and goals can be set in the dashboard

#### Existing User:
* Click login link on homepage

* New page renders to display login form

* Once logged in, users are taken to their dashboards which uses AJAX and
javascript/jQuery for a dynamic user experience

* The user dashboard has three sections: 'User Profile', 'My HobbyHabits',
and 'Social'

* _User Profile:_ User can update their personal info and opt in for text
message reminders

* _My HobbyHabits:_ User can select the HobbyHabit they want to interact with
and track new completions, set/view goal, view/edit/delete past completions in a
table, and view their progress via 3 data-visualizations created with chart.js

* _Social:_ This feature requires that the user provide their zipcode and has a
minimun of 1 HobbyHabit. User can select the HobbyHabit they want to interact
with to get a list of events (using the Eventbrite API) in their area related to
the seleceted HobbyHabit 