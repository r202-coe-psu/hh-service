from flask import abort
from flask_jwt_extended import JWTManager

from hhservice.api import models

from .renderers import render_json


def init_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
            return {'roles': user.roles}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
            return str(user.id)

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        try:
            user = models.User.objects.with_id(identity)
        except Exception as e:
            errors = [
                        {
                            'status': '403',
                            'title':  'The user might not have the necessary permissions for a resource',
                            'detail': 'The user might not have the necessary permissions for a resource'
                        }
                    ]

            response_dict = dict(errors=errors)
            response = render_json(response_dict)
            response.status_code = 403
            abort(response)
        # print('user jwt', user)
        return user
