import mongoengine as me
import datetime

from passlib.hash import bcrypt


class User(me.Document):

    username = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    status = me.StringField(required=True)
    roles = me.ListField(me.StringField(), default=['user'])

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.now,
                                    auto_now=True)

    meta = {'collection': 'users'}

    def __get_salt(self, salt):
        token = salt.replace(' ', '.')
        return '{:.<22.22}'.format(token)

    def set_password(self, password, salt=''):
        self.password = bcrypt.using(rounds=16).hash(password,
                                    salt=self.__get_salt(salt))

    def verify_password(self, password, salt=''):
        return bcrypt.verify(password,
                             self.password)
