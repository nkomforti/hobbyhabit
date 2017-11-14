"""Utility file to seed hobbyhabbit database."""

import datetime

from model import User, Completion, UserHobby, Hobby, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "User"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    for i, row in enumerate(open("seed-data/u.user")):
        row = row.rstrip()

        (first_name,
         last_name,
         email,
         username,
         password,
         phone,
         zipcode) = row.split("|")

        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    phone=phone,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_hobbies():
    """Load hobbies from u.hobby into database."""

    print "Hobby"

    Hobby.query.delete()

    for i, row in enumerate(open("seed-data/u.hobby")):
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

    for i, row in enumerate(open("seed-data/u.userhobby")):
        row = row.rstrip()

        (user_id,
         hobby_id,
         goal_start_date_str,
         goal_active,
         goal_freq_num,
         goal_freq_time_unit) = row.split("|")

        # The date is in the file as daynum-month_abbreviation-year;
        # we need to convert it to an actual datetime object.
        if goal_start_date_str:
            goal_start_date = datetime.datetime.strptime(goal_start_date_str,
                                                         "%d-%m-%Y")
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

        # import pdb; pdb.set_trace()

        user_hobby = UserHobby(goal_start_date=goal_start_date,
                               user_id=user_id,
                               hobby_id=hobby_id,
                               goal_active=goal_active,
                               goal_freq_num=goal_freq_num,
                               goal_freq_time_unit=goal_freq_time_unit)

        # We need to add to the session or it won't ever be stored
        db.session.add(user_hobby)

        # provide some sense of progress
        if i % 1000 == 0:
            print i
            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.
            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()


def load_completions():
    """Load completions from u.completion into database."""

    print "Completion"

    Completion.query.delete()

    with open("seed-data/u.completion") as completions_data:

        for i, completion_data in enumerate(completions_data):
            completion_data = completion_data.rstrip()
            date_str, total_practice_time, notes = completion_data.split("|")

            date = datetime.datetime.strptime(date_str, "%d-%m-%Y")

            if total_practice_time:
                total_practice_time = int(total_practice_time)
            else:
                total_practice_time = None

            completion = Completion(date=date,
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
    load_completions()
