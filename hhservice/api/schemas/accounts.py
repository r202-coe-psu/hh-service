import marshmallow as ma
from marshmallow_jsonapi import Schema, fields

class UserSchema(Schema):

    id = fields.String(dump_only=True)
    username = ma.fields.String(required=True,
            validator=ma.validate.Length(min=3, max=20))
    password = ma.fields.String(required=True,
            validator=ma.validate.Length(min=6, max=50))
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


    class Meta:
        type_ = 'user'
        strict = True


