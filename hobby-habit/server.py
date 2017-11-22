"""HobbyHabit."""

from jinja2 import StrictUndefined
from flask import Flask, g, url_for, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Completion, Hobby, UserHobby, Goal
from functools import wraps


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined  # Raises an error if an undefined variable is used in Jinja 2.
app.jinja_env.auto_reload = True  # What does this do??
app.secret_key = "ABC"  # Required to use Flask sessions and the debug toolbar.


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:  # g is short for global
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


@app.route('/login', methods=['GET'])
def display_login_form():
    """Display login form."""

    return render_template("login-form.html")


@app.route('/login', methods=['POST'])
def process_login_form():
    """Process login form."""

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


@app.route('/update-user-profile', methods=['POST'])
@login_required
def process_user_profile_form():
    """Process user-profile form and save changes to db."""

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

    return "success"


@app.route('/update-password-dashboard', methods=['POST'])
def process_update_password_dashboard():
    """Process update-password form in dashboard, user-profile and commit to db.
    """

    pass


@app.route('/add-completion', methods=['POST'])
@login_required
def process_add_completion():
    """Process tracker form and add new completion to database for selected
    user_hobby_id.
    """

    completion_date = request.form["completion-date"]
    total_hours = int(request.form["total-hours"])
    total_minutes = int(request.form["total-minutes"])
    completion_notes = request.form["completion-notes"]
    current_user_hobby_id = request.form["user-hobby-id"]

    new_completion = Completion()

    new_completion.completion_date = completion_date
    new_completion.total_practice_time = ((total_hours * 60) + total_minutes)
    new_completion.notes = completion_notes
    new_completion.user_hobby_id = current_user_hobby_id

    db.session.add(new_completion)
    db.session.commit()

    # import pdb; pdb.set_trace()

    return "success"


@app.route('/view-completions.json', methods=['GET'])
def display_completions():
    """Get completions data from db for selected user_hobby to display."""

    for use to display data as vis and non-vis

    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    current_user_hobby_id = # Get user id that was clicked

    user_hobby_completions = db.session.query(Completion).filter(Completion.user_hobby_id == current_user_hobby_id).all()

    current_user_data = current_user.get_user_data()
    user_hobby_completions = current_user_data["user_hobbies"]

    pass

    # return render_template('dashboard.html',
    #                        user_hobby_completions=user_hobby_completions)


@app.route('/mult-hobbies-vis.json', methods=['GET'])
def display_mult_hobbies_vis():
    """Get completion data from db for all of the current user's user_hobbies
    and create data vis.
    """

    pass


@app.route('/add-hobby-dashboard', methods=['POST'])
def process_add_hobby_dashboard():
    """Process add-hobby form in dashboard, my-hobbyhabits and commit to db."""

    pass


@app.route('/add-goal-dashboard', methods=['POST'])
def process_add_goal_dashboard():
    """Process add-goal form in dashboard, my-hobbyhabits and commit to db."""

    pass


@app.route('/view-current-goal.json', methods=['GET'])
def display_current_goal():
    """Get goal data from db for selected user_hobby to display."""

    # for use to display data as vis and non-vis

    pass


@app.route('/social.json', methods=['GET', 'POST'])  # not sure wwhich to use yet
def display_social_events():
    """Get and display local events related to selected user_hobby."""

    pass


@app.route('/settings', methods=['POST'])  # May not use.
def process_settings():
    """Process settings-form."""

    pass


@app.route('/register', methods=['POST'])
def register_user():
    """Process registration form and add user to database."""

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


@app.route('/add-hobby', methods=['GET'])
@login_required
def display_add_hobby_form():
    """Display add-hobby form."""

    return render_template("add-hobby.html")


@app.route('/add-hobby', methods=['POST'])
@login_required
def process_add_hobby_form():
    """Process add-hobby form."""

    # Get current user from session.
    current_user_id = session["user_id"]

    # Get data from form.
    num_hobbies = request.form["num-hobbies"]

    # Make as many new goals as user adds to form.
    for hobby_num in range(int(num_hobbies)):

        # Get hobby name, see if it's in the DB
        hobby_name = request.form.get("hobby-name-" + str(hobby_num + 1))
        hobby_obj = Hobby.query.filter(Hobby.hobby_name == hobby_name).first()

        # If hobby not in the DB, add to DB.
        if not hobby_obj:
            hobby_obj = Hobby(hobby_name=hobby_name)
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


@app.route('/add-goal', methods=['GET'])
@login_required
def display_add_goal_form():
    """Display add-goal form."""

    # Get current user from session.
    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    # Render add goal template and pass list of hobbies to Jinja template.
    return render_template("add-goal.html",
                           current_user_hobbies=current_user.hobbies,  # CHANGE TO .user_hobbies???
                           current_user=current_user)


@app.route('/add-goal', methods=['POST'])
@login_required
def process_add_goal_form():
    """Process add-goal form."""

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
                                                Goal.goal_active.is_(True)).first()  # or Goal.goal_active == True).first()

    if active_goal:
        active_goal.goal_active = False

    db.session.commit()

    return "Success"  # Javascript is redirecting to /dashboard.


@app.route('/logout', methods=["GET"])
def logout():
    """Log out."""

    del session["user_id"]
    flash("Log out successful")

    return redirect("/")


################################################################################


if __name__ == "__main__":

    app.debug = True
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
