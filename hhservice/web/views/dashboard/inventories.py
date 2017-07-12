from flask import (Blueprint,
                   render_template,
                   g,
                   redirect,
                   url_for,
                   session,
                   request)
from flask_login import login_required

from hhservice.web import forms

module = Blueprint('dashboard.inventories',
                   __name__,
                   url_prefix='/inventories'
                   )

def get_building(building_id):
    for b in session.get('buildings'):
        if b['id'] == building_id:
            return b

@module.route('')
@login_required
def index():
    return render_template('/dashboard/inventories/index.html')


@module.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = forms.inventories.InventoryForm()
    if not form.validate_on_submit():
        return render_template('dashboard/inventories/create.html',
                               form=form)
    c = g.get_hhapps_client('inventory')
    building = get_building(request.args.get('building_id'))

    inventory = c.inventories.create(building=building,
                                     **form.data)

    if inventory.is_error:
        return render_template('dashboard/inventories/create.html',
                               form=form,
                               errors=inventory.errors)

    return redirect(url_for('dashboard.inventories.view',
                            inventory_id=inventory.id))


@module.route('/<inventory_id>')
@login_required
def view(inventory_id):

    c = g.get_hhapps_client('inventory')
    inventory = c.inventories.get(inventory_id)

    return render_template('/dashboard/inventories/view.html',
                           inventory=inventory)
