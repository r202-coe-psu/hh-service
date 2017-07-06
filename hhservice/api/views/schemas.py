from flask import Blueprint
import marshmallow_jsonschema as mjs
import marshmallow_jsonapi as mja
from marshmallow import fields
import datetime

from hhservice.api.renderers import render_json
from hhservice.api import schemas

module = Blueprint('schemas', __name__, url_prefix='/schemas')


class JSONAPISchema(mjs.JSONSchema):

    def get_properties(self, obj):
        mapping = {v: k for k, v in obj.TYPE_MAPPING.items()}
        mapping[fields.Email] = mjs.base.text_type
        mapping[fields.Dict] = dict
        mapping[fields.List] = list
        mapping[fields.Url] = mjs.base.text_type
        mapping[fields.LocalDateTime] = datetime.datetime
        properties = {}

        for field_name, field in sorted(obj.fields.items()):
            if hasattr(field, '_jsonschema_type_mapping'):
                schema = field._jsonschema_type_mapping()
            elif field.__class__ in mapping:
                pytype = mapping[field.__class__]
                schema = self.__class__._from_python_type(field, pytype)
            elif isinstance(field, fields.Nested):
                schema = self.__class__._from_nested_schema(field)
            elif isinstance(field, mja.fields.Relationship):
                # print(field_name, field)
                try:
                    schema = self.__class__._from_relationship_type(field)
                except Exception as e:
                    print(e)
            else:
                raise ValueError('unsupported field type %s' % field)

            # Apply any and all validators that field may have
            for validator in field.validators:
                if validator.__class__ in mjs.base.FIELD_VALIDATORS:
                    schema = mjs.base.FIELD_VALIDATORS[validator.__class__](
                        schema, field, validator, obj
                    )

            properties[field.name] = schema

        # print('properties', properties)
        new_properties = {}
        for k, v in properties.items():
            if 'type' in v and v['type'] == 'array':
                field = obj.fields[k].container.__class__
                if field == fields.String:
                    v['items'] = dict(type='string')
            if 'title' in v:
                v['title'] = schemas.common.dasherize(v['title'])

            new_properties[schemas.common.dasherize(k)] = v
        return new_properties

    def get_required(self, obj):
        required = [t.replace('_', '-') for t in super().get_required(obj)]

        return required

    @classmethod
    def _from_relationship_type(cls, field):
        schema = cls().dump(field).data

        if field.metadata.get('metadata', {}).get('description'):
            schema['description'] = (
                field.metadata['metadata'].get('description')
            )

        if field.metadata.get('metadata', {}).get('title'):
            schema['title'] = field.metadata['metadata'].get('title')

        sub_schema = cls().dump(field._Relationship__schema()).data

        if field.many:
            schema = {
                'type': ["array"] if field.required else ['array', 'null'],
                'items': sub_schema,
            }

        return schema


@module.route('')
def all():
    json_schema = JSONAPISchema()

    schema_list = schemas.__all__

    all_schemas = {}
    for schema in schema_list:
        all_schemas[schema.Meta.type_] = json_schema.dump(schema()).data

    return render_json(all_schemas)
