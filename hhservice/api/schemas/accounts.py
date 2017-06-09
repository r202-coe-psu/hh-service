import marshmallow as ma
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class UserSchema(Schema):

    id = fields.String(dump_only=True)
    username = ma.fields.String(required=True,
                                validator=ma.validate.Length(min=3, max=20))
    password = ma.fields.String(load_only=True, required=True,
                                validator=ma.validate.Length(min=6, max=50))
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    status = fields.String(requred=True, default='unregister')

    class Meta:
        type_ = 'user'
        strict = True
