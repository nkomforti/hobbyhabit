"""Utility file to seed hobbyhabbit database."""

import datetime
from sqlalchemy import func

from model import User, Completion, UserHobby, Hobby, connect_to_db, db
from server import app

# write load functions to add data to database
# dont forget to: db.session.add(data_being_added) and then db.session.commit()


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
