import marshmallow as ma
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from . import common
from .applications import ApplicationSchema
from .users import UserSchema


class BuildingSchema(Schema):

    id = fields.String(dump_only=True)
    name = fields.String(required=True,
                         validator=ma.validate.Length(min=3, max=20))
    description = fields.String()
    tags = fields.List(fields.String())

    status = fields.String(requred=True, default='deactive')

    owner = fields.Relationship(
            related_url='/users/{user_id}',
            related_url_kwargs={'user_id': '<id>'},
            many=False,
            schema=UserSchema,
            include_resource_linkage=True,
            type_='users',
            dump_only=True
            )
    members = fields.Relationship(
            related_url='/users/{user_id}',
            related_url_kwargs={'user_id': '<id>'},
            many=True,
            schema=UserSchema,
            include_resource_linkage=True,
            type_='members',
            dump_only=True
            )
    applications = fields.Relationship(
            related_url='/applications/{application_id}',
            related_url_kwargs={'application_id': '<id>'},
            many=True,
            schema=ApplicationSchema,
            include_resource_linkage=True,
            type_='applications',
            dump_only=True
            )

    created_date = fields.DateTime(dump_only=True)
    updated_date = fields.DateTime(dump_only=True)

    class Meta:
        type_ = 'buildings'
        strict = True
        inflect = common.dasherize
