"""HobbyHabit."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Completion, Goal, Hobby


app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined  # Raises an error if an undefined variable is used in Jinja 2.

app.jinja_env.auto_reload = True  # What does this do??

app.secret_key = "ABC"  # Required to use Flask sessions and the debug toolbar.


@app.route('/', methods=['GET'])
def homepage():
    """Display homepage."""

    return render_template("homepage.html")


@app.route('/welcome', methods=['POST'])
def welcome_user():
    """Display welcome page for user to add hobbies and habits."""

    # Get form variables.
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Create new User and assign it data.
    new_user = User()
    new_user.user_name = username
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

        return redirect("/welcome/%s" % new_user.user_id)

# change to register??
@app.route("/welcome/<int:user_id>", methods=['GET'])
def show_add_hobbies_form(user_id):
    """Show Welcome page for given user and display add hobbies form."""

    user_id = session.get("user_id")

    return render_template("add-hobbies.html", user_id=user_id)


@app.route("/add-hobbies", methods=["POST"])
def add_hobbies():
    """Process add hobbies form."""

    # Get data from form
    num_hobbies = request.form["num-hobbies"]

    # Make as many new goals as user adds to form.
    for hobby_num in range(num_hobbies):

        # Get hobby name, see if it's in the DB
        hobby_name = request.form.get("hobby-name-" + str(hobby_num + 1))
        hobby_obj = Hobby.query.filter(Hobby.hobby_name == hobby_name).first()

        # If hobby not in the DB, add to DB.
        if not hobby_obj:
            hobby_obj = Hobby(hobby_name=hobby_name)
            db.session.add(hobby_obj)
            db.session.commit()

    return render_template("add-goals.html")






@app.route("/register", methods=["POST"])
def register_user():
    # get info from form

    #add to to DB

    return redirect("/add-hobbies")

























@app.route('/register', methods=['GET'])
def register_form():
    """Display registration form for user sign up."""

    return render_template("registration-form.html")  # Should take you to user's profile page and display the fields that need to be added?? instead of a different form. The completed forms shoul show content and the rest left blank.


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

    # if not user:
    #     flash("No such user") 
    #     return redirect("/login")


    # if user.password != password: flash("Incorrect password") return redirect("/login")
    #     session["user_id"] = user.user_id
    #     flash("Logged in")
    # return redirect("/users/%s" % user.user_id)




    # return render_template("welcome.html")

if __name__ == "__main__":

    app.debug = True
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
