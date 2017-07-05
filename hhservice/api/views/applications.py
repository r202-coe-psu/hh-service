from flask import Blueprint

from hhservice.api import schemas
from hhservice.api import models
from hhservice.api.renderers import render_json


module = Blueprint('applications', __name__, url_prefix='/applications')


@module.route('', methods=['GET'])
@module.route('/', methods=['GET'])
def list_applications():
    schema = schemas.ApplicationSchema(many=True)

    apps = models.Application.objects(status='active')
    return render_json(schema.dump(apps).data)


@module.route('/<application_id>', methods=['GET'])
@module.route('/<application_id>/', methods=['GET'])
def get(application_id):
    schema = schemas.ApplicationSchema()

    try:
        app = models.Application.objects.with_id(application_id)
    except Exception as e:
        raise e

    return render_json(schema.dump(app).data)
