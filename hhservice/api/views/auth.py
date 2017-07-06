
import datetime

from flask import Blueprint, request, abort

from hhservice.api.renderers import render_json
from hhservice.api import models

import mongoengine as me
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                current_user,
                                jwt_refresh_token_required,
                                )
from flask_jwt_extended.tokens import decode_jwt
from flask_jwt_extended.config import config as jwtconfig

module = Blueprint('auth', __name__, url_prefix='/auth')


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
    if user:
        if user.verify_password(password):
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)

            jwt_data = decode_jwt(access_token,
                                  jwtconfig.secret_key,
                                  jwtconfig.algorithm,
                                  jwtconfig.csrf_protect)

            token = dict(
                methods=['password'],
                user=dict(
                    id=user.id,
                    name=name
                    ),
                access_token=access_token,
                refresh_token=refresh_token,
                issued_date=datetime.datetime.utcnow(),
                expiry_date=datetime.datetime.utcfromtimestamp(
                    jwt_data.get('exp'))
                )
            return render_json(token)

    errors = [
        {
          'status': '401',
          'title':  'User or Password mismatch',
          'detail': 'User or Password mismatch'
        }
    ]

    response_dict = request.get_json()
    response_dict['errors'] = errors

    response = render_json(response_dict)
    response.status_code = 401
    abort(response)


@module.route('/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    user = current_user

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    jwt_data = decode_jwt(access_token,
                          jwtconfig.secret_key,
                          jwtconfig.algorithm,
                          jwtconfig.csrf_protect)

    token = dict(
        access_token=access_token,
        refresh_token=refresh_token,
        issued_date=datetime.datetime.utcnow(),
        expiry_date=datetime.datetime.utcfromtimestamp(
            jwt_data.get('exp'))
        )

    return render_json(token)
