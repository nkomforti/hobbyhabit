"""Utility file to seed hobbyhabbit database."""

import datetime
from sqlalchemy import func

from model import User, Completion, UserHobby, Hobby, connect_to_db, db
from server import app

# write load functions to add data to database
# dont forget to: db.session.add(data_being_added) and then db.session.commit()
def load_users():
    """Load users from u.user into database."""

    print "Users"

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


def load_user_hobbies():
    """Load user hobbies from u.userhobby into database."""

    print "User Hobbies"

    for i, row in enumerate(open("seed-data/u.userhobby")):
        row = row.rstrip()

        (goal_start_date_str,
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

        user_hobby = UserHobby(goal_start_date=goal_start_date,
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


def load_hobbies():
    """Load hobbies from u.hobby into database."""

    pass


def load_completions():
    """Load completions from u.completion into database."""

    pass


def set_user_id():
    """Set value for the next user_id after seeding the database."""

    # Get the Max user_id in the database.
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id +1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # call load functions here
    set_user_id()
