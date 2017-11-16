"""HobbyHabit."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Completion, Hobby, UserHobby, Goal


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined  # Raises an error if an undefined variable is used in Jinja 2.
app.jinja_env.auto_reload = True  # What does this do??
app.secret_key = "ABC"  # Required to use Flask sessions and the debug toolbar.


@app.route('/', methods=['GET'])
def homepage():
    """Display homepage."""

    return render_template("homepage.html")


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
def display_add_hobby_form():
    """Display add-hobby form."""

    return render_template("add-hobby.html")


@app.route('/process-hobby', methods=['POST'])
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
def display_add_goal_form():
    """Display add-goal form."""

    # Get current user from session.
    current_user_id = session["user_id"]

    current_user = User.query.get(current_user_id)

    # # Get subquery object of hobby ids for current user from DB.
    # current_user_hobby_ids_obj = db.session.query(UserHobby.hobby_id).filter(UserHobby.user_id == current_user_id).subquery()
    # # Get list of hobby names for current user by user-hobby ids from DB.
    # current_user_hobbies = db.session.query(Hobby.hobby_name).filter(Hobby.hobby_id.in_(current_user_hobby_ids_obj)).all()

    # Render add goal template and pass list of hobbies to Jinja template.
    return render_template("add-goal.html",
                           current_user_hobbies=current_user.hobbies,
                           current_user=current_user)


@app.route('/add-goal', methods=['POST'])
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


@app.route('/dashboard', methods=['GET'])
def display_dashboard():
    """Display user's dashboard."""

    return render_template("dashboard.html")


@app.route('/login', methods=['GET'])
def login_form():
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


@app.route('/logout')
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
