from flask import Blueprint, request, g, render_template, redirect, url_for
from flask_login import login_required

from hhservice.web import forms

module = Blueprint('dashboard.buildings', __name__, url_prefix='/buildings')


@module.route('/')
@login_required
def index():
    c = g.hhclient
    buildings = c.building.list()
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

    return redirect(url_for('dashboard.buildings.view',
                            building_id=building.id))


@module.route('/<building_id>', methods=['GET'])
@login_required
def view(building_id):
    c = g.hhclient
    building = c.buildings.get(building_id)
    return render_template('/dashboard/buildings/view.html',
                           building=building)


