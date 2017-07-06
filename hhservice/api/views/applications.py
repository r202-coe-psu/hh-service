from flask import Blueprint, request

from hhservice.api import schemas
from hhservice.api import models
from hhservice.api.renderers import render_json


module = Blueprint('applications', __name__, url_prefix='/applications')


def get_application_error_not_found():
    response_dict = request.get_json()
    errors = [
        {
            'status': '404',
            'title':  'Application not found',
            'detail': 'Application not found'
        }
    ]
    response_dict.update(errors=errors)
    response = render_json(response_dict)
    response.status_code = 404

    return response


@module.route('', methods=['GET'])
def list_applications():
    schema = schemas.ApplicationSchema(many=True)

    apps = models.Application.objects(status='active')
    return render_json(schema.dump(apps).data)


@module.route('/<application_id>', methods=['GET'])
def get(application_id):
    schema = schemas.ApplicationSchema()

    try:
        app = models.Application.objects.with_id(application_id)
    except Exception as e:
        raise e

    return render_json(schema.dump(app).data)
