from flask import Blueprint
import marshmallow_jsonschema as mjs
import marshmallow_jsonapi as mja
from marshmallow import fields
import datetime

from hhservice.api.renderers import render_json
from hhservice.api import schemas
from hhservice.api import json_schemas

module = Blueprint('schemas', __name__, url_prefix='/schemas')



@module.route('')
def all():
    json_schema = json_schemas.JSONAPISchema()

    schema_list = schemas.__all__

    all_schemas = {}
    for schema in schema_list:
        all_schemas[schema.Meta.type_] = json_schema.dump(schema()).data

    return render_json(all_schemas)
