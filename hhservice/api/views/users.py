
from flask import Blueprint, request, abort

from hhservice.api.renderers import render_json
from hhservice.api import models
from hhservice.api import schemas
from hhservice.api import app

import mongoengine as me

module = Blueprint('users', __name__, url_prefix='/users')


@module.route('/', methods=['post'])
def create():
    schema = schemas.UserSchema()
    try:
        user_data = schema.load(request.get_json())
    except Exception as e:
        response = render_json(schema.dump(request.get_json()).data)
        response.status_code = 400
        abort(response)

    user = models.User.objects(me.Q(username=user_data.data['username']) |
                               me.Q(email=user_data.data['email'])).first()
    if user is None:
        user = models.User(**user_data.data)
        user.set_password(user_data.data['password'],
                          salt=app.secret_key)
        user.status = 'active'
        user.save()
        return render_json(schema.dump(user).data)

    errors = [
        {
          'status': '400',
          'title':  'Found User in System',
          'detail': 'User name or email found in system'
        }
    ]

    response_dict = schema.dump(user_data.data).data
    response_dict['errors'] = errors

    response = render_json(response_dict)
    response.status_code = 400
    abort(response)


@module.route('/<user_id>', methods=['get'])
def get(user_id):
    schema = schemas.UserSchema()
    user = models.User.objects.get(user_id)

    return render_json(schema.dump(user).data)
