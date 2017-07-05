import marshmallow as ma
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from . import common


class ApplicationSchema(Schema):

    id = fields.String(dump_only=True)
    name = fields.String(required=True,
                         validator=ma.validate.Length(min=3, max=20))
    description = fields.String()
    detail = fields.String()

    publicurl = fields.URL(required=True)
    status = fields.String(requred=True, default='deactivate')

    created_date = fields.DateTime(dump_only=True)
    updated_date = fields.DateTime(dump_only=True)

    class Meta:
        type_ = 'applications'
        strict = True
        inflect = common.dasherize
