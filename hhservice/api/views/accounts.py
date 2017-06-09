
from flask import Blueprint, request, abort

from hhservice.api.renderers import render_json
from hhservice.api.schemas import accounts
from hhservice.api import models

module = Blueprint('accounts', __name__)


@module.route('/register', methods=['post'])
def register():
    schema = accounts.UserSchema()
    try:
        user_data = schema.load(request.get_json())
    except:
        response = render_json(schema.dump(request.get_json()))
        response.status_code = 500
        abort(response)

    user = models.User.objects.filter(
        username=user_data.data['username']).first()

    if not user:
        user = models.User.objects.filter(
            email=user_data.data['email']).first()

    if not user:
        user = models.User(**user_data.data)
        user.status = 'active'
        user.save()
        return render_json(schema.dump(user))
    response = render_json(schema.dump(user_data))
    response.status_code = 500
    abort(response)
