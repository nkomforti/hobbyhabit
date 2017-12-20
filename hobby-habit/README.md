# HobbyHabit
HobbyHabit is a hobby/task tracking application that lets users track their progress for any activity they want to hold themselves more accountable for. Users can set goals based on what they want to achieve, schedule text reminders, find events where they can socialize with others in their area interested in the same activities, and toggle between several data visualizations that make analyzing the details of their progress easy and approachable, so that marveling at their hard work is a snap and they can get back to getting things done! 

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

## How to Run Locally
*HobbyHabit is not deployed*

* Create a python virtual environment and install all dependencies

`$ pip install -r requirements.txt`

* Create a database called hobbyhabit:

`$ createdb hobbyhabit`

Create the tables in the database:
`$ python model.py`
Start Flask server:
`$ python server.py`
Access the web app at localhost:5000