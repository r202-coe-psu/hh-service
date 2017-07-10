from flask import Blueprint, render_template, g, redirect, url_for
from flask_login import login_required

from hhservice.web import forms

module = Blueprint('dashboard.inventories',
                   __name__,
                   url_prefix='/inventories'
                   )


@module.route('')
@login_required
def index():
    return render_template('/dashboard/inventories/index.html')


@module.route('/create')
@login_required
def create():
    form = forms.inventories.InventoryForm()
    if not form.validate_on_submit():
        return render_template('dashboard/inventories/create.html',
                               form=form)
    c = g.hhclient
    inventory = c.buildings.create(**form.data)

    if inventory.is_error:
        return render_template('dashboard/inventories/create.html',
                               form=form,
                               errors=inventory.errors)

    return redirect(url_for('dashboard.inventories.view',
                            inventory_id=inventory.id))


@module.route('/<inventory_id>')
@login_required
def view(inventory_id):

    return render_template('/dashboard/inventories/view.html')
