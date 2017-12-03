"""HobbyHabit."""

from jinja2 import StrictUndefined
from flask import (Flask, g, url_for, render_template, request,
                   flash, redirect, session, jsonify)
from titlecase import titlecase

# from pprint import pformat
import os
import requests
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Completion, Hobby, UserHobby, Goal
from functools import wraps


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined  # Raises an error if an undefined variable is used in Jinja 2.
app.jinja_env.auto_reload = True
app.secret_key = "ABC"  # Required to use Flask sessions and the debug toolbar.

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')
EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

# TODO: Add more comments, clean up route names and view function names.


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:  # g is short for global.
            return redirect(url_for('process_login_form', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Runs before every server request.
@app.before_request
def before_request():
    user_id = session.get("user_id")

    if not user_id:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@app.route('/', methods=['GET'])
def homepage():
    """Display homepage."""

    return render_template("homepage.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Display/process login form."""

    if request.method == 'GET':
        return render_template("login-form.html")

    else:
        # Get data from form.
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Invalid username")
            return redirect("/login")

        if user.password != password:
            flash("Invalid password")
            return redirect("/login")

        session["user_id"] = user.user_id

        flash("Login successful")

        return redirect("/dashboard")


@app.route('/dashboard', methods=['GET'])
@login_required
def display_dashboard():
    """Display user's dashboard."""

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    current_user_data = current_user.get_user_data()

    return render_template("dashboard.html",
                           current_user=current_user,
                           current_user_data=current_user_data)


@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Process user-profile form."""

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    zipcode = request.form["zipcode"]
    phone_number = request.form["phone-number"]
    text_reminder = request.form["txt-opt-in-out"]

    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.zipcode = zipcode
    current_user.phone = phone_number

    if text_reminder == "on":
        current_user.text_reminder = True
    else:
        current_user.text_reminder = False

    db.session.add(current_user)
    db.session.commit()

    return "Success"


@app.route('/update-password-dashboard', methods=['POST'])
def update_password():
    """Process update-password form located in dashboard.
    """

    pass


@app.route('/add-completion', methods=['POST'])
@login_required
def add_completion():
    """Process add-completion form for selected user_hobby_id."""

    completion_date = request.form["completion-date"]
    total_hours = int(request.form["total-hours"])
    total_minutes = int(request.form["total-minutes"])
    notes = request.form["notes"]
    current_user_hobby_id = request.form["user-hobby-id"]

    new_completion = Completion()

    new_completion.completion_date = completion_date
    new_completion.total_practice_time = ((total_hours * 60) + total_minutes)
    new_completion.notes = notes
    new_completion.user_hobby_id = current_user_hobby_id

    db.session.add(new_completion)
    db.session.commit()

    return "Success"


@app.route('/get-hobbies.json', methods=['GET'])
def get_hobbies():
    """Get list of hobby names for autocomplete in add-hobby forms."""

    hobbies = Hobby.query.filter(Hobby.autocomplete == True).all()

    hobby_names = []

    for hobby in hobbies:
        hobby_names.append(hobby.hobby_name)

    return jsonify(hobby_names)


@app.route('/get-completions.json', methods=['GET'])
def get_completions():
    """Get completions data for selected user_hobby to display in dashboard."""

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    user_hobby_id = int(request.args["user-hobby-id"])

    current_user_data = current_user.get_user_data()

    # completions = {}

    for user_hobby in current_user_data["user_hobbies"]:
        if user_hobby["user_hobby_id"] == user_hobby_id:
            completions = user_hobby["completions"]

    return jsonify(completions)


@app.route('/get-completions-line-vis.json', methods=['GET'])
def get_completions_line_vis():
    """Get completions data for selected user_hobby for line chart data vis."""

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    user_hobby_id = int(request.args["user-hobby-id"])

    current_user_data = current_user.get_user_data()

    for user_hobby in current_user_data["user_hobbies"]:
        if user_hobby["user_hobby_id"] == user_hobby_id:
            completions = user_hobby["completions"]
            hobby_name = user_hobby["hobby_name"]

    total_practice_times = []
    completion_dates = []

    for completion in completions:
        total_practice_times.append(completion['total_practice_time'])

    for completion in completions:
        completion_dates.append(completion['completion_date'])

    data = {"hobby_name": hobby_name,
            "total_practice_times": total_practice_times,
            "completion_dates": completion_dates}

    return jsonify(data)


@app.route('/get-user-hobby-completions-by-year.json', methods=['GET'])
def get_user_hobby_completions_by_year():
    """Get completions data for selected user_hobby by year chart/data vis."""

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    user_hobby_id = int(request.args["user-hobby-id"])

    current_user_data = current_user.get_user_data()

    for user_hobby in current_user_data["user_hobbies"]:
        if user_hobby["user_hobby_id"] == user_hobby_id:
            completions = user_hobby["completions"]
            hobby_name = user_hobby["hobby_name"]

    total_practice_times = []
    completion_dates = []

    for completion in completions:
        total_practice_times.append(completion['total_practice_time'])  # format with strftime

    for completion in completions:
        completion_dates.append(completion['completion_date'])

    completion_data = dict(zip(completion_dates, total_practice_times))
    completion_data = completion_data.items()

    completions_by_year = {}

    for date, time in completion_data:
        year = date.year
        if year not in completions_by_year:
            completions_by_year[year] = []
        elif year in completions_by_year and date.year == year:
            completions_by_year[year].extend([(date, time)])

    for year in completions_by_year:
        for completion in completions_by_year[year]:
            completions_by_year[year].sort()

    years = []
    total_hours_per_year = []
    total_completions_per_year = []

    for year in completions_by_year:
        years.append(year)

    for year in completions_by_year:
        total_completions_per_year.append(len(completions_by_year[year]))

    for year in completions_by_year:
        total_hours_per_year.append(sum(comp[1] for comp in completions_by_year[year])/60)

    data = {"hobby_name": hobby_name,
            "years": years,
            "total_hours_per_year": total_hours_per_year,
            "total_completions_per_year": total_completions_per_year}

    return jsonify(data)


@app.route('/get-mult-hobbies-vis.json', methods=['GET'])
def get_mult_hobbies_vis():
    """Get completion data for all of the current user's user_hobbies and create
    data visualization.
    """

    # TODO: This is just for demo. Add data by year after demo.

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    current_user_data = current_user.get_user_data()

    completions = {}

    completion_count = []
    hobby_names = []

    for user_hobby in current_user_data["user_hobbies"]:
        hobby_names.append(user_hobby["hobby_name"])
        completions[user_hobby["user_hobby_id"]] = []
        for completion in user_hobby["completions"]:
            completions[user_hobby["user_hobby_id"]].append(completion)

    for completion in completions:
        completion_count.append(len(completions[completion]))

    data = {"hobby_names": hobby_names,
            "completion_count": completion_count}

    return jsonify(data)


@app.route('/add-hobby-dashboard', methods=['POST'])
def add_hobby_dashboard():
    """Process add-hobby form in dashboard."""

    # Get current user from session.
    current_user_id = session["user_id"]

    # Get data from form.
    new_user_hobby_name = request.form["new-hobbyhabit-name"]
    hobby_obj = Hobby.query.filter(Hobby.hobby_name == new_user_hobby_name).first()

    if not hobby_obj:
        hobby_obj = Hobby(hobby_name=new_user_hobby_name,
                          autocomplete=False)
        db.session.add(hobby_obj)
        db.session.commit()

    user_hobby_obj = UserHobby.query.filter(UserHobby.hobby_id == hobby_obj.hobby_id,
                                            UserHobby.user_id == current_user_id).first()

    if not user_hobby_obj:
        user_hobby_obj = UserHobby(user_id=current_user_id,
                                   hobby_id=hobby_obj.hobby_id)
        db.session.add(user_hobby_obj)
        db.session.commit()

    user_hobby_id = {"id": user_hobby_obj.user_hobby_id}

    return jsonify(user_hobby_id)


@app.route('/add-goal-dashboard', methods=['POST'])
def process_add_goal_dashboard():
    """Process add-goal form located in dashboard."""

    # Get data from form.
    goal_start_date = request.form["goal-start-date"]
    goal_freq_num = request.form["goal-freq-num"]
    goal_freq_time_unit = request.form["goal-freq-time-unit"]
    current_user_hobby_id = request.form["user-hobby-id"]

    new_goal = Goal(goal_start_date=goal_start_date,
                    goal_freq_num=goal_freq_num,
                    goal_freq_time_unit=goal_freq_time_unit,
                    user_hobby_id=current_user_hobby_id,
                    goal_active=True)

    active_goal = db.session.query(Goal).filter(Goal.user_hobby_id == current_user_hobby_id,
                                                Goal.goal_active.is_(True)).first()
    db.session.add(new_goal)

    if active_goal:
        active_goal.goal_active = False

    db.session.commit()

    return "Success"


@app.route('/get-active-goal.json', methods=['GET'])
def get_active_goal():
    """Get active_goal data for selected user_hobby to display in dashboard."""

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    user_hobby_id = int(request.args["user-hobby-id"])

    current_user_data = current_user.get_user_data()

    goal_data = {}

    for user_hobby in current_user_data["user_hobbies"]:
        if user_hobby["user_hobby_id"] == user_hobby_id:
            goal_data["active_goal"] = user_hobby["active_goal"]
            goal_data["inactive_goals"] = user_hobby["inactive_goals"]

    return jsonify(goal_data)


@app.route('/get_social_events.json', methods=['GET'])
def get_social_events():
    """Search for local events related to selected user_hobby."""

    # Get current user_id from session.
    current_user_id = session["user_id"]
    # Get user object by user_id.
    current_user = User.query.get(current_user_id)
    # Get user_hobby_id from click event.
    current_user_hobby_id = int(request.args["user-hobby-id"])
    # Get hobby_name from db by user_hobby_id.
    hobby_name = db.session.query(Hobby.hobby_name).join(UserHobby).filter(UserHobby.hobby_id == Hobby.hobby_id,
                                                                           UserHobby.user_hobby_id == current_user_hobby_id).one()
    # Get zipcode of user object.
    zipcode = current_user.zipcode
    # Preset distance for API request.
    distance = "25mi"

    # Preset sort for API request.
    sort = "best"

    # If the required information is in the request, look for events.
    if zipcode and hobby_name:

        payload = {'q': hobby_name,
                   'location.address': zipcode,
                   'location.within': distance,
                   'sort_by': sort,
                   }

        # Send API token.
        headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

        response = requests.get(EVENTBRITE_URL + "events/search/",
                                params=payload,
                                headers=headers)
        data = response.json()

        # Check if the response was successful (status code of less than 400).
        if response.ok:
            # If ok, use the list of events from the returned JSON.
            data = data

        # If error (status code between 400 and 600), use an empty dictionary
        else:
            data = {}

        return jsonify(data)  # Results.

    # If the required info isn't in request, redirect to the user profile form.
    else:
        return "Does not meet requirements"  # Results.


@app.route('/register', methods=['POST'])
def register_user():
    """Process registration form."""

    # Get data from form.
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Create new User and assign it data.
    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.password = password

    user = User.query.filter_by(email=email).first()  # Returns None if not in DB, which is Falsey.

    # Check if user already exists in DB. If account exists, redirect to login.
    if user:
        flash("An account with that email already exists")
        return redirect("/login")

    # Otherwise add user to DB, flash confirmation, and save user to session.
    else:
        db.session.add(new_user)
        db.session.commit()

        flash("Account successfully created")
        session["user_id"] = new_user.user_id

        return redirect("/add-hobby")


@app.route('/add-hobby', methods=['GET', 'POST'])
@login_required
def add_hobby():
    """Display/process add-hobby form."""

    if request.method == 'GET':

        autocomplete_hobby_objects = db.session.query(Hobby).filter(Hobby.autocomplete == True).all()

        return render_template("add-hobby.html",
                               autocomplete_hobby_objects=autocomplete_hobby_objects)

    else:
        # Get current user from session.
        current_user_id = session["user_id"]

        # Get data from form.
        num_hobbies = titlecase(request.form["num-hobbies"])

        # Make as many new goals as user adds to form.
        for hobby_num in range(int(num_hobbies)):

            # Get hobby name, see if it's in the DB
            hobby_name = request.form.get("hobby-name-" + str(hobby_num + 1))
            hobby_obj = Hobby.query.filter(Hobby.hobby_name == hobby_name).first()

            # If hobby not in the DB, add to DB.
            if not hobby_obj:
                hobby_obj = Hobby(hobby_name=hobby_name,
                                  autocomplete=False)  # Check this line.
                db.session.add(hobby_obj)
                db.session.commit()

            user_hobby_obj = UserHobby.query.filter(UserHobby.hobby_id == hobby_obj.hobby_id,
                                                    UserHobby.user_id == current_user_id).first()

            if not user_hobby_obj:
                user_hobby_obj = UserHobby(user_id=current_user_id,
                                           hobby_id=hobby_obj.hobby_id)
                db.session.add(user_hobby_obj)
                db.session.commit()

        return redirect("/add-goal")


@app.route('/add-goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    """Display/process add-goal form."""

    if request.method == 'GET':

        # Get current user from session.
        current_user_id = session["user_id"]

        current_user = User.query.get(current_user_id)

        # Render add goal template and pass list of hobbies to Jinja template.
        return render_template("add-goal.html",
                               current_user_hobbies=current_user.hobbies,
                               current_user=current_user)

    else:
        # Get current user from session.
        current_user_id = session["user_id"]

        # Get data from form.
        goal_start_date = request.form["goal-start-date"]
        goal_freq_num = request.form["goal-freq-num"]
        goal_freq_time_unit = request.form["goal-freq-time-unit"]
        hobby_id = request.form["hobby-id"]

        user_hobby_id = db.session.query(UserHobby).filter(UserHobby.user_id == current_user_id,
                                                           UserHobby.hobby_id == hobby_id).one().user_hobby_id

        new_goal = Goal(goal_start_date=goal_start_date,
                        goal_freq_num=goal_freq_num,
                        goal_freq_time_unit=goal_freq_time_unit,
                        user_hobby_id=user_hobby_id,
                        goal_active=True)

        db.session.add(new_goal)

        active_goal = db.session.query(Goal).filter(Goal.user_hobby_id == user_hobby_id,
                                                    Goal.goal_active.is_(True)).first()

        if active_goal:
            active_goal.goal_active = False

        db.session.commit()

        return "Success"  # Javascript is redirecting to /dashboard.


@app.route('/logout', methods=["GET"])
def logout():
    """Log current user out."""

    del session["user_id"]
    flash("Log out successful")

    return redirect("/")


################################################################################


if __name__ == "__main__":

    app.debug = True
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
