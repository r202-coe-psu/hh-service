from flask import Blueprint
from marshmallow_jsonschema import JSONSchema
from marshmallow import fields

from hhservice.api.renderers import render_json
from hhservice.api import schemas

module = Blueprint('schemas', __name__, url_prefix='/schemas')


class JSONAPISchema(JSONSchema):

    def get_properties(self, obj):
        properties = super().get_properties(obj)
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


@module.route('/')
@module.route('')
def all():
    json_schema = JSONAPISchema()

    schema_list = [schemas.UserSchema(),
                   schemas.AuthSchema(),
                   schemas.TokenSchema()]

    all_schemas = {}
    for schema in schema_list:
        all_schemas[schema.Meta.type_] = json_schema.dump(schema).data

    return render_json(all_schemas)
