"""HobbyHabit."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, User, Completion, Goal, Hobby


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

app.secret_key = "ABC"  # Required to use Flask sessions and the debug toolbar.

# Raises an error if an undefined variable is used in Jinja 2.


@app.route('/')
def homepage():
    """Display homepage."""

    return render_template("homepage.html")


@app.route('/remaining-registration/<username>', methods=['POST'])
def partial_registration(username):
    """Display remaining registration form.

    User will only see this page if sign up was started directly on homepage and
    not by clicking on 'Sign up' link in the homepage header, which renders
    complete registration form.

    """

    return render_template("partial-registration-form.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Display registration form for user signup."""

    return render_template("complete-registration-form.html")


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
