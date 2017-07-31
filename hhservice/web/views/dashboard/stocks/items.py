from flask import (Blueprint,
                   render_template,
                   g,
                   redirect,
                   url_for,
                   request)

from hhservice.web import forms

module = Blueprint('dashboard.stocks.items',
                   __name__,
                   url_prefix='/items')


@module.route('')
def index():
    c = g.get_hhapps_client('stock')
    items = c.items.list()

    form = forms.stocks.items.ItemUPCForm()

    return render_template('/dashboard/stocks/items/index.html',
                           form=form,
                           items=items)


@module.route('/upc', methods=['POST'])
def get_upc():
    form = forms.stocks.items.ItemUPCForm()
    if not form.validate_on_submit():
        return render_template('/dashboard/stocks/items/index.html',
                               form=form)

    return redirect(url_for('dashboard.stocks.items.view_upc',
                            upc=form.upc.data,
                            **request.args))


@module.route('/<item_id>')
def view(item_id):
    c = g.get_hhapps_client('stock')
    item = c.items.get(item_id)

    form = forms.stocks.items.ItemUPCForm()

    return render_template('/dashboard/stocks/items/view_upc.html',
                           item=item,
                           form=form)


@module.route('/upc/<upc>')
def view_upc(upc):
    c = g.get_hhapps_client('stock')
    item = c.items.get_upc(upc)

    form = forms.stocks.items.ItemUPCForm()

    return render_template('/dashboard/stocks/items/view_upc.html',
                           item=item,
                           form=form)


@module.route('/add')
def add():
    c = g.get_hhapps_client('stock')
    items = c.items.list()

    form = forms.stocks.items.ItemForm()

    return render_template('/dashboard/stocks/items/add.html',
                           form=form,
                           items=items)
