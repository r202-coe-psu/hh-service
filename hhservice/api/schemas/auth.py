from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class UserAuthSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String()
    password = fields.String(load_only=True)

    class Meta:
        type_ = 'user'
        strict = True


class PasswordAuthSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserAuthSchema)

    class Meta:
        type_ = 'password'
        strict = True


class IdentitySchema(Schema):
    id = fields.String(dump_only=True)
    methods = fields.List(fields.String())
    password = fields.Nested(PasswordAuthSchema)

    class Meta:
        type_ = 'identity'
        strict = True


class AuthSchema(Schema):
    id = fields.String(dump_only=True)
    identity = fields.Nested(IdentitySchema)

    class Meta:
        type_ = 'auth'
        strict = True


class TokenSchema(Schema):
    id = fields.String(dump_only=True)
    methods = fields.String()
    audit_id = fields.String()
    user = fields.Nested(UserAuthSchema)
    issused_date = fields.DateTime()
    expires_date = fields.DateTime()

    class Meta:
        type_ = 'token'
        strict = True
