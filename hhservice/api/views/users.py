
from flask import Blueprint, request, abort, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from hhservice.api.renderers import render_json
from hhservice.api import models
from hhservice.api import schemas

import mongoengine as me

module = Blueprint('users', __name__, url_prefix='/users')


@module.route('/', methods=['post'])
@module.route('', methods=['post'])
def create():
    schema = schemas.UserSchema()
    try:
        user_data = schema.load(request.get_json())
    except Exception as e:
        print(e)
        response_dict = request.get_json()
        response_dict.update(e.messages)
        response = render_json(response_dict)
        response.status_code = 400
        abort(response)

    user = models.User.objects(me.Q(username=user_data.data['username']) |
                               me.Q(email=user_data.data['email'])).first()
    if user is None:
        user = models.User(**user_data.data)
        user.set_password(user_data.data['password'],
                          salt=current_app.secret_key)
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
@module.route('/<user_id>/', methods=['get'])
@jwt_required
def get(user_id):
    current_user = get_jwt_identity()
    print(current_user)

    schema = schemas.UserSchema()
    try:
        user = models.User.objects.with_id(user_id)
    except Exception as e:

        errors = [
            {
              'status': '404',
              'title':  'User not found',
              'detail': 'User not found'
            }
        ]

        response_dict = dict(errors=errors)
        response = render_json(response_dict)
        response.status_code = 404
        abort(response)

    return render_json(schema.dump(user).data)
