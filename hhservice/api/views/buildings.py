from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, current_user

from hhservice.api import models
from hhservice.api import schemas
from hhservice.api.renderers import render_json

module = Blueprint('buildings', __name__, url_prefix='/buildings')


def get_building_error_not_found():
    response_dict = request.get_json()
    errors = [
        {
            'status': '404',
            'title':  'Building not found',
            'detail': 'Building not found'
        }
    ]
    response_dict.update(errors=errors)
    response = render_json(response_dict)
    response.status_code = 404

    return response


@module.route('', methods=['POST'])
@jwt_required
def create():
    schema = schemas.BuildingSchema()
    try:
        building_data = schema.load(request.get_json())
    except Exception as e:
        response_dict = request.get_json()
        response_dict.update(e.messages)
        response = render_json(response_dict)
        response.status_code = 400
        abort(response)

    owner = current_user._get_current_object()
    building = models.Building(owner=owner,
                               status='active',
                               **building_data.data)
    building.save()

    return render_json(schema.dump(building).data)


@module.route('', methods=['GET'])
@jwt_required
def list():
    schema = schemas.BuildingSchema(many=True)
    owner = current_user._get_current_object()
    buildings = models.Building.objects(owner=owner)
    return render_json(schema.dump(buildings).data)


@module.route('/<building_id>', methods=['GET'])
@jwt_required
def get(building_id):
    schema = schemas.BuildingSchema()
    owner = current_user._get_current_object()
    building = models.Building.objects(id=building_id,
                                       owner=owner).first()
    if not building:
        return abort(get_building_error_not_found())

    return render_json(schema.dump(building).data)


@module.route('/<building_id>', methods=['DELETE'])
@jwt_required
def delete(building_id):
    owner = current_user._get_current_object()
    building = models.Building.objects(id=building_id,
                                       owner=owner).first()
    if not building:
        return abort(get_building_error_not_found())

    building.delete()

    return render_json()


@module.route('/<building_id>/applications', methods=['PUT'])
@jwt_required
def activate_application(building_id):
    owner = current_user._get_current_object()
    building = models.Building.objects(id=building_id,
                                       owner=owner).first()
    if not building:
        return abort(get_building_error_not_found())

    try:
        schema = schemas.ApplicationSchema()
        app_dict = schema.load(request.get_json(), partial=True).data
        application = models.Application.objects.with_id(app_dict['id'])
    except Exception as e:
        from . import applications
        return abort(applications.get_application_error_not_found())

    activated_application = models.ActivatedApplication(
            id=application.id,
            owner=owner,
            application=application)
    building.activated_applications.append(activated_application)
    building.save()

    schema = schemas.BuildingSchema()
    return render_json(schema.dump(building).data)


@module.route('/<building_id>/applications/<application_id>',
              methods=['DELETE'])
@jwt_required
def deactivate_application(building_id, application_id):
    owner = current_user._get_current_object()
    building = models.Building.objects(id=building_id,
                                       owner=owner).first()
    if not building:
        return abort(get_building_error_not_found())

    building.activated_applications = [
        aa for aa in building.activated_applications
        if str(aa.id) != application_id]
    building.save()

    return render_json()
