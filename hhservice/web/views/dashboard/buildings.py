from flask import Blueprint, session, g, render_template, redirect, url_for
from flask_login import login_required

from hhservice.web import forms

module = Blueprint('dashboard.buildings', __name__, url_prefix='/buildings')


@module.route('/')
@login_required
def index():
    c = g.hhclient
    buildings = c.buildings.list()
    return render_template('/dashboard/buildings/index.html',
                           buildings=buildings)


@module.route('/create', methods=['POST', 'GET'])
@login_required
def create():

    form = forms.buildings.BuildingForm()
    if not form.validate_on_submit():
        return render_template('dashboard/buildings/create.html',
                               form=form)
    c = g.hhclient
    building = c.buildings.create(**form.data)

    if building.is_error:
        return render_template('dashboard/buildings/create.html',
                               form=form,
                               errors=building.errors)

    buildings = session['buildings']
    buildings.append(building.data)
    session['buildings'] = buildings

    return redirect(url_for('dashboard.buildings.view',
                            building_id=building.id))


@module.route('/<building_id>', methods=['GET'])
@login_required
def view(building_id):
    c = g.hhclient
    building = c.buildings.get(building_id)
    applications = c.applications.list()

    return render_template('/dashboard/buildings/view.html',
                           building=building,
                           applications=applications)


@module.route('/<building_id>/applications/<application_id>/<status>',
              methods=['GET'])
@login_required
def control_applications(building_id, application_id, status):
    c = g.hhclient
    if status == 'activate':
        c.buildings.activate_application(
                building_id,
                application_id)
    elif status == 'deactivate':
        c.buildings.deactivate_application(
                building_id,
                application_id)
    return redirect(url_for('dashboard.buildings.view',
                            building_id=building_id))
