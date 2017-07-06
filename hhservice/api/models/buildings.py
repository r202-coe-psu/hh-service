import mongoengine as me
import datetime

from . import applications
from . import users


class ActivatedApplication(me.EmbeddedDocument):
    id = me.ObjectIdField()
    application = me.ReferenceField(applications.Application,
                                    required=True,
                                    dbref=True)
    owner = me.ReferenceField(users.User,
                              required=True,
                              dbref=True)
    activated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)


class Building(me.Document):

    name = me.StringField(required=True)
    description = me.StringField()
    tags = me.ListField(me.StringField())

    owner = me.ReferenceField(users.User, required=True, dbref=True)
    members = me.ListField(me.ReferenceField(users.User,
                                             required=True,
                                             dbref=True))
    activated_applications = me.ListField(
        me.EmbeddedDocumentField(ActivatedApplication)) 

    status = me.StringField(required=True, default='deactivate')

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'buildings'}
