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

    # Define relationship to hobbies.
    hobbies = db.relationship("Hobby",
                              secondary="user_hobbies",
                              backref=db.backref("users"))

    # # change this
    # # Define relationship to user_hobbies.
    # goals = db.relationship("UserHobby",
    #                         primaryjoin=("and_(UserHobby.user_id == User.user_id,"
    #                                      + " UserHobby.goal_active == True)"),
    #                         backref=db.backref("users"))

    # # Define relationship to completions table.
    # completions = db.relationship("Completion",
    #                               primaryjoin="UserHobby.user_id == User.user_id",
    #                               secondaryjoin="UserHobby.user_hobby_id == Completion.user_hobby_id",
    #                               viewonly=True,
    #                               backref=db.backref("users"))

    # def get_hobby_data_by_user(self):
    #     """Gets helpful hobby data about a particular user object."""

    #     {"hobby_id": {"completions": [...],
    #                   "goal_freq_num": ...,
    #                   "goal_freq_time_unit": ...,}
    #      "...": {"...": ...,
    #              "...": ...,
    #              "...": ...}}

    def __repr__(self):
        """Provide helpful representation about a User when printed."""

        s = "<User user_id=%s email=%s username=%s>"

        return s % (self.user_id,
                    self.email,
                    self.username)


class UserHobby(db.Model):
    """Association table to bridge users and hobbies."""

    __tablename__ = "user_hobbies"

    user_hobby_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    hobby_id = db.Column(db.Integer,
                         db.ForeignKey("hobbies.hobby_id"))

    # Define relationship to completions table.
    completions = db.relationship("Completion",
                                  order_by="Completion.date",
                                  backref=db.backref("user_hobbies"))

    def __repr__(self):
        """Provide helpful representation aboout UserHobby when printed."""

        s = "<UserHobby user_hobby_id=%s user_id=%s hobby_id=%s>"

        return s % (self.user_hobby_id,
                    self.users.user_id,
                    self.hobbies.hobby_id)


class Hobby(db.Model):
    """User hobby/habit."""

    __tablename__ = "hobbies"

    hobby_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    hobby_name = db.Column(db.String(64),
                           nullable=False)
    autocomplete = db.Column(db.Boolean,
                             default=False,
                             nullable=False)  # No autocompletion for user added hobbies/habits. In seed.py will set non-user-added hobbies/habits to True.

    def __repr__(self):
        """Provide helpful representation about Hobby when printed."""

        s = "<Hobby hobby_id=%s hobby_name=%s>"

        return s % (self.hobby_id,
                    self.hobby_name)


class Goal(db.Model):
    """"""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_hobby_id = db.Column(db.Integer,
                              db.ForeignKey("user_hobbies.user_hobby_id"))
    goal_start_date = db.Column(db.DateTime,
                                nullable=True)
    goal_active = db.Column(db.Boolean,
                            default=False,
                            nullable=False)
    goal_freq_num = db.Column(db.Integer,
                              nullable=True)  # Number of times per...
    goal_freq_time_unit = db.Column(db.Enum("Day",
                                            "Week",
                                            "Month",
                                            "Year",
                                            name="goal_freq_time_unit"),
                                    nullable=True)  # Day/Week/Month/Year.

    # Define relationship to user_hobbies table.
    user_hobby = db.relationship("UserHobby",
                                 order_by="Goal.goal_start_date",
                                 backref=db.backref("goals"))

    def __repr__(self):
        """Provide helpful representation about Goal when printed."""

        s = "<Goal goal_id=%s hobby_id=%s user_id=%s>"

        return s % (self.goal_id,
                    self.user_hobby.hobby_id,
                    self.user_hobby.user_id)


class Completion(db.Model):
    """Completion log of user hobby/habbit."""

    __tablename__ = "completions"

    completion_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    user_hobby_id = db.Column(db.Integer,
                           db.ForeignKey("user_hobbies.user_hobby_id"))
    date = db.Column(db.DateTime,
                     nullable=False)
    total_practice_time = db.Column(db.Integer,
                                    nullable=True)
    notes = db.Column(db.Text,
                      nullable=True)

    def __repr__(self):
        """Provide helpful representation about Completion when printed."""

        s = "<Completion completion_id=%s user_id=%s hobby_id=%s>"

        return s % (self.completion_id,
                    self.user_hobby.user_id,
                    self.user_hobby.hobby_id)


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

    app = Flask(__name__)  # Dummy instance of Flask class. Using this instead of: from server import app
    connect_to_db(app)  # Connect database to Flask app
    db.create_all()  # Create database
    print "Connected to DB."
