"""Models and database functions for HobbyHabit project."""

from flask_sqlalchemy import SQLAlchemy

from flask import Flask

db = SQLAlchemy()


################################################################################
# Model definitions.

class User(db.Model):
    """User of HobbyHabit website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    first_name = db.Column(db.String(25),
                           nullable=True,)
    last_name = db.Column(db.String(25),
                          nullable=True)
    email = db.Column(db.String(64),
                      unique=True,
                      nullable=False)
    username = db.Column(db.String(15),
                         unique=True,
                         nullable=False)
    password = db.Column(db.String(64),
                         nullable=False)
    phone = db.Column(db.String(15),
                      nullable=True)
    zipcode = db.Column(db.String(15),
                        nullable=True)

    def __repr__(self):
        """Provide helpful representation about user when printed."""

        s = "<User user_id=%s email=%s username=%s>"

        return s % (self.user_id, self.email, self.username)


class Completion(db.Model):
    """Completion log of user hobby/habbit."""

    __tablename__ = "completions"

    completion_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    goal_id = db.Column(db.Integer,
                        db.ForeignKey('goals.goal_id'))
    date = db.Column(db.DateTime,
                     nullable=False)
    notes = db.Column(db.Text,
                      nullable=True)

    goal = db.relationship("Goal",
                           backref=db.backref("completions"))

    def __repr__(self):
        """Provide helpful representation about completed hobby/habbit when printed.
        """

        s = '<Completion completion_id=%s goal_id=%s>'

        return s % (self.completion_id, self.goal_id)


class Goal(db.Model):
    """User hobby/habit goal."""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    hobby_id = db.Column(db.Integer,
                         db.ForeignKey('hobbies.hobby_id'))
    goal_frequency_num = db.Column(db.Integer,
                                   nullable=False)  # Number of times per...
    goal_frequency_time_unit = db.Column(db.String(5),
                                         db.Enum('Day',
                                                 'Week',
                                                 'Month',
                                                 'Year',
                                                 name='goal_frequency_time_unit'),
                                         nullable=False)  # day/week/month/year

    # Define relationship to user.
    user = db.relationship("User",
                           backref=db.backref("goals"))

    # Define relationship to hobby/habbit.
    hobby = db.relationship("Hobby",
                            backref=db.backref("hobbies"))

    def __repr__(self):
        """Provide helpful representation about user goal when printed."""

        s = '<Goal goal_id=%s user_id=%s hobby_id=%s>'

        return s % (self.goal_id, self.user_id, self.hobby_id)


class Hobby(db.Model):
    """User hobby/habit."""

    __tablename__ = "hobbies"

    hobby_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    hobby_name = db.Column(db.String(64),
                           nullable=False)
    autocomplete = db.Column(db.Boolean,
                             default=False)  # No autocompletion for user added hobbies/habits. In seed.py will set non-user-added hobbies/habits to True.

    def __repr__(self):
        """Provide helpful representation about a hobby/habit when printed."""

        s = '<Hobby hobby_id=%s hobby_name=%s>'

        return s % (self.hobby_id, self.hobby_name)


################################################################################
# Helper functions.

def connect_to_db(app):
    """Conect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hobbyhabit'  # postgres: or postgresql??
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    app = Flask(__name__)  # dummy instance of Flask class. Using this instead of: from server import app
    connect_to_db(app)
    print "Connected to DB."
