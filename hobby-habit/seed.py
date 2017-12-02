"""Utility file to seed hobbyhabbit database."""

import datetime

from model import User, Completion, UserHobby, Hobby, Goal, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "User"

    # Delete all rows in table, so that if running this a second time it won't
    # try to add duplicate users.
    User.query.delete()

    for i, row in enumerate(open("seed-data/user.txt")):
        row = row.rstrip()

        (first_name,
         last_name,
         email,
         username,
         password,
         phone,
         text_reminder,
         zipcode) = row.split("|")

        if not text_reminder:
            text_reminder = False
        else:
            text_reminder = True

        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    phone=phone,
                    text_reminder=text_reminder,
                    zipcode=zipcode)

        # Add user to the session so it will be stored.
        db.session.add(user)

        # Provide some sense of progress.
        if i % 100 == 0:
            print i

    # Commit to db.
    db.session.commit()


def load_hobbies():
    """Load hobbies from u.hobby into database."""

    print "Hobby"

    Hobby.query.delete()

    for i, row in enumerate(open("seed-data/hobby.txt")):
        row = row.rstrip()

        hobby_name, autocomplete = row.split("|")

        if autocomplete:
            autocomplete = True
        else:
            autocomplete = False

        hobby = Hobby(hobby_name=hobby_name,
                      autocomplete=autocomplete)

        db.session.add(hobby)

        if i % 100 == 0:
            print i

    db.session.commit()


def load_user_hobbies():
    """Load user hobbies from u.userhobby into database."""

    print "UserHobby"

    UserHobby.query.delete()

    for i, row in enumerate(open("seed-data/userhobby.txt")):
        row = row.rstrip()

        user_id, hobby_id = row.split("|")

        user_hobby = UserHobby(user_id=user_id,
                               hobby_id=hobby_id)

        db.session.add(user_hobby)

        if i % 1000 == 0:
            print i
            # NOTE: for optimization--committing after every add, wiil cause the
            # database to do a lot of work committing each record. However, if
            # waiting until the end, on computers with smaller amounts of memory
            # it might thrash around. Committing every 1,000th add is a good balance.
            db.session.commit()

    db.session.commit()


def load_goals():
    """Load goals from u.goal into database."""

    print "Goal"

    Goal.query.delete()

    with open("seed-data/goal.txt") as goals_data:

        for i, goal_data in enumerate(goals_data):
            goal_data = goal_data.rstrip()

            (user_hobby_id,
             goal_start_date_str,
             goal_active,
             goal_freq_num,
             goal_freq_time_unit) = goal_data.split("|")

            # Convert date string to a datetime object.
            if goal_start_date_str:
                goal_start_date = datetime.datetime.strptime(goal_start_date_str,
                                                             "%Y-%m-%d %H:%M:%S")
            else:
                goal_start_date = None

            if goal_freq_num:
                goal_freq_num = int(goal_freq_num)
            else:
                goal_freq_num = None

            if not goal_freq_time_unit:
                goal_freq_time_unit = None

            if not goal_active:
                goal_active = None

            goal = Goal(user_hobby_id=user_hobby_id,
                        goal_start_date=goal_start_date,
                        goal_active=goal_active,
                        goal_freq_num=goal_freq_num,
                        goal_freq_time_unit=goal_freq_time_unit)

            db.session.add(goal)

            if i % 100 == 0:
                print i

        db.session.commit()


def load_completions():
    """Load completions from u.completion into database."""

    print "Completion"

    Completion.query.delete()

    with open("seed-data/completion.txt") as completions_data:

        for i, completion_data in enumerate(completions_data):
            completion_data = completion_data.rstrip()
            user_hobby_id, completion_date_str, total_practice_time, notes = completion_data.split("|")

            completion_date = datetime.datetime.strptime(completion_date_str, "%Y-%m-%d %H:%M:%S")

            if total_practice_time:
                total_practice_time = int(total_practice_time)
            else:
                total_practice_time = None

            completion = Completion(user_hobby_id=user_hobby_id,
                                    completion_date=completion_date,
                                    total_practice_time=total_practice_time,
                                    notes=notes)

            db.session.add(completion)

            if i % 100 == 0:
                print i

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_hobbies()
    load_user_hobbies()
    load_goals()
    load_completions()
