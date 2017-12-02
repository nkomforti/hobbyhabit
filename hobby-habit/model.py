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
    text_reminder = db.Column(db.Boolean,
                              default=False,
                              nullable=False)
    zipcode = db.Column(db.String(15),
                        nullable=True)

    # Define relationship to hobbies.
    hobbies = db.relationship("Hobby",
                              secondary="user_hobbies",
                              backref=db.backref("users"))
    # Define relationship to goals.
    goals = db.relationship("Goal",
                            primaryjoin="User.user_id==UserHobby.user_id",
                            secondary="user_hobbies",
                            secondaryjoin="UserHobby.user_hobby_id==Goal.user_hobby_id")
    # Define relationship to goals.
    active_goals = db.relationship("Goal",
                                   primaryjoin="User.user_id==UserHobby.user_id",
                                   secondary="user_hobbies",
                                   secondaryjoin="and_(UserHobby.user_hobby_id==Goal.user_hobby_id, Goal.goal_active==True)")
    # Define relationship to completions.
    completions = db.relationship("Completion",
                                  primaryjoin="User.user_id==UserHobby.user_id",
                                  secondary="user_hobbies",
                                  secondaryjoin="UserHobby.user_hobby_id==Completion.user_hobby_id")
    # Define relationship to user_hobbies.
    user_hobbies = db.relationship("UserHobby",
                                   primaryjoin="User.user_id==UserHobby.user_id",
                                   backref=db.backref("user"))

    def get_user_data(self):
        """Gets helpful data for a particular user in the form of a dictionary.
        """

        user_data = {"user_id": self.user_id,
                     "username": self.username,
                     "user_hobbies": []}

        user_hobbies = self.user_hobbies

        for user_hobby in user_hobbies:
            hobby_info = {}
            hobby_info["user_hobby_id"] = user_hobby.user_hobby_id
            hobby_info["hobby_name"] = db.session.query(Hobby.hobby_name).join(UserHobby).filter(UserHobby.hobby_id == Hobby.hobby_id, UserHobby.user_hobby_id == user_hobby.user_hobby_id).one()
            hobby_info["completions"] = []
            hobby_info["inactive_goals"] = []
            hobby_info["active_goal"] = []

            user_data["user_hobbies"].append(hobby_info)

            for completion in user_hobby.completions:
                completion_info = {}
                completion_info['completion_id'] = completion.completion_id
                completion_info['completion_date'] = completion.completion_date
                completion_info['total_practice_time'] = completion.total_practice_time
                completion_info['notes'] = completion.notes

                hobby_info["completions"].append(completion_info)

            for goal in user_hobby.goals:
                goal_info = {}
                goal_info["goal_id"] = goal.goal_id
                goal_info["goal_start_date"] = goal.goal_start_date
                goal_info["goal_freq_num"] = goal.goal_freq_num
                goal_info["goal_freq_time_unit"] = goal.goal_freq_time_unit
                goal_info["goal_active"] = goal.goal_active

                if goal.goal_active:
                    hobby_info["active_goal"].append(goal_info)
                else:
                    hobby_info["inactive_goals"].append(goal_info)

        return user_data

    def __repr__(self):
        """Provide helpful representation about a User when printed."""

        s = "<User user_id=%s email=%s username=%s>"

        return s % (self.user_id,
                    self.email,
                    self.username)


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
                             nullable=False)  # Autocomplete=False for all user added hobbyhabits.

    def __repr__(self):
        """Provide helpful representation about Hobby when printed."""

        s = "<Hobby hobby_id=%s hobby_name=%s>"

        return s % (self.hobby_id,
                    self.hobby_name)


class UserHobby(db.Model):
    """Association table to bridge users and hobbies."""

    __tablename__ = "user_hobbies"

    user_hobby_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    hobby_id = db.Column(db.Integer,
                         db.ForeignKey("hobbies.hobby_id"),
                         nullable=False)

    def __repr__(self):
        """Provide helpful representation aboout UserHobby when printed."""

        s = "<UserHobby user_hobby_id=%s user_id=%s hobby_id=%s>"

        return s % (self.user_hobby_id,
                    self.user_id,
                    self.hobby_id)


class Goal(db.Model):
    """"""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_hobby_id = db.Column(db.Integer,
                              db.ForeignKey("user_hobbies.user_hobby_id"),
                              nullable=False)
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
                                 backref=db.backref("goals"))  # change to goal

    def __repr__(self):
        """Provide helpful representation about Goal when printed."""

        s = "<Goal goal_id=%s user_hobby_id=%s goal_active=%s>"

        return s % (self.goal_id, self.user_hobby_id, self.goal_active)


class Completion(db.Model):
    """Completion log of user hobby/habit."""

    __tablename__ = "completions"

    completion_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    user_hobby_id = db.Column(db.Integer,
                              db.ForeignKey("user_hobbies.user_hobby_id"),
                              nullable=False)
    completion_date = db.Column(db.DateTime,
                                nullable=False)
    total_practice_time = db.Column(db.Integer,
                                    nullable=True)
    notes = db.Column(db.Text,
                      nullable=True)

    # Define relationship to user_hobbies table.
    user_hobby = db.relationship("UserHobby",
                                 order_by="Completion.completion_date",
                                 backref=db.backref("completions"))

    def __repr__(self):
        """Provide helpful representation about Completion when printed."""

        s = "<Completion completion_id=%s hobby_id=%s>"

        return s % (self.completion_id, self.user_hobby_id)


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
    # db.create_all()  # Create database
    print "Connected to DB."
