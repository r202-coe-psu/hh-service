import rethinkengine as re
import datetime


class User(re.Document):
    __table_name__ = 'users'

    username = re.StringField(required=True, unique=True)
    password = re.StringField(required=True)
    email = re.StringField(required=True, unique=True)
    first_name = re.StringField(required=True)
    last_name = re.StringField(required=True)
    status = re.StringField(required=True)

    created_date = re.DateTimeField(required=True,
                                    default=datetime.datetime.now())
    updated_date = re.DateTimeField(required=True,
                                    default=datetime.datetime.now())
