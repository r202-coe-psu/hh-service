import mongoengine as me
import datetime


class Application(me.Document):

    name = me.StringField(required=True, unique=True)
    description = me.StringField()
    detail = me.StringField()

    publicurl = me.URLField(required=True)
    status = me.StringField(required=True, default='deactivate')

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'applications'}
