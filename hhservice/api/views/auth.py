
import datetime

from flask import Blueprint, request, abort, current_app

from hhservice.api.renderers import render_json
from hhservice.api import models
from hhservice.api import schemas

import mongoengine as me
from flask_jwt_extended import create_access_token, get_jwt_identity

module = Blueprint('auth', __name__, url_prefix='/auth')


@module.route('/', methods=['post'])
@module.route('', methods=['post'])
def auth():
    auth_dict = request.get_json()['auth']
    try:
        name = auth_dict['identity']['password']['user']['name']
        password = auth_dict['identity']['password']['user']['password']
    except Exception as e:
        response_dict = request.get_json()
        response_dict.update(e.messages)
        response = render_json(response_dict)
        response.status_code = 400
        abort(response)

    
    user = models.User.objects(me.Q(username=name) |
                               me.Q(email=name)).first()
    td = datetime.timedelta(hours=6)
    if user:
        if user.verify_password(password):
            identity = dict(
                id=str(user.id),
                name=user.username,
                roles=user.roles)

            access_token = create_access_token(identity)

            token = dict(
                methods=['password'],
                expires_date=datetime.datetime.now() + td,
                user=dict(
                    id=user.id,
                    name=name
                    ),
                access_token=access_token,
                issued_date=datetime.datetime.now()
                )
            return render_json(token)

    errors = [
        {
          'status': '400',
          'title':  'User or Password mismatch',
          'detail': 'User or Password mismatch'
        }
    ]

    response_dict = request.get_json()
    response_dict['errors'] = errors

    response = render_json(response_dict)
    response.status_code = 404
    abort(response)