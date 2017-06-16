from flask import Blueprint
from marshmallow_jsonschema import JSONSchema

from hhservice.api.renderers import render_json
from hhservice.api.schemas import users

module = Blueprint('schemas', __name__, url_prefix='/schemas')



@module.route('/')
def all():
    json_schema = JSONSchema()
    
    user_schema = users.UserSchema()
    all_schemas = {
            user_schema.Meta.type_:json_schema.dump(user_schema).data
            }

    return render_json(all_schemas)
