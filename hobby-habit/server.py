"""HobbyHabit."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, User, Completion, Goal, Hobby


app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined  # Raises an error if an undefined variable is used in Jinja 2.

app.jinja_env.auto_reload = True  # What does this do??

app.secret_key = "ABC"  # Required to use Flask sessions and the debug toolbar.


@app.route('/')
def homepage():
    """Display homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Display registration form for user sign up."""

    return render_template("registration-form.html")  # Should take you to user's profile page and display the fields that need to be added?? instead of a different form. The completed forms shoul show content and the rest left blank.


@app.route('/welcome')
def welcome_user():
    """Display welcome page for user to add hobbies and habits."""

    return render_template("welcome.html")


@app.route('welcome', methods=['POST'])
def process_welcome_form():
    """Process welcom form and add user hobbies to database."""

    hobby_habit = request.form.get("hobby-habit")
    pass

@app.route('/register', methods=['POST'])
def process_register_form():
    """Process registration form and add user to database."""

    # Get form variables.
    first_name = request.form.get("first-name")  # can also be written as: first_name = request.form["first-name"]
    last_name = request.form.get("last-name")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    zipcode = request.form.get("zipcode")

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    phone=phone,
                    zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User, %s, successfully registered." % username)
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Display login form."""

    return render_template("login-form.html")


@app.route('/login', methods=['POST'])
def process_login_form():
    """Process login form."""

    # Get form variables.
    username = request.form.get(username)  # accept username for sign up first and then add logic to give the option of loging in with both username and email later on.
    password = request.form.get(password)

    user = User.query.filter_by(username=username).first()

    if not user:
        pass


if __name__ == "__main__":

    app.debug = True
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
