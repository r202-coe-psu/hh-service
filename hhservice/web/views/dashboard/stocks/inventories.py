from flask import Blueprint, render_template, g, redirect, url_for
from hhservice.web import forms

import datetime

module = Blueprint('dashboard.stocks.inventories',
                   __name__,
                   url_prefix='/<stock_id>/inventories')


@module.route('/add', methods=['GET', 'POST'])
def add(stock_id):
    c = g.get_hhapps_client('stock')
    stock = c.stocks.get(stock_id)
    items = c.items.list()

    item_choices = [(item.id, '{} ({})'.format(item.name, item.upc)) for item
                    in items]
    item_choices.insert(0, ('', 'Select item or enter UPC'))
    form = forms.stocks.inventories.InventoryForm()
    form.item.choices = item_choices
    form.expired_date.label.text = '{}: default date is {}'.format(
            form.expired_date.label.text,
            form.expired_date.default.ctime())
    # if not form.expired_date.data:
    #     form.expired_date.data = form.expired_date.default.strftime(
    #             form.expired_date.format)

    is_item = True if form.item.data else False or len(form.item_upc.data) > 0
    print('fdata', form.data)
    if not form.validate_on_submit():
        print('ferror', form.errors)
        errors = [{'detail': '{}: {}'.format(k, v) } for k, v 
                  in form.errors.items()]
        return render_template('/dashboard/stocks/inventories/add.html',
                               form=form,
                               stock=stock,
                               items=items)
    if not is_item:
        errors = [{'detail': 'Select item or enter upc'}]
        return render_template('/dashboard/stocks/inventories/add.html',
                               form=form,
                               errors=errors,
                               stock=stock,
                               items=items)
    data = form.data
    if len(data['item']) > 0:
        data['item'] = {'id': data['item']}

    inventory = c.inventories.create(stock=stock, **data)
    if inventory.is_error:
        # import pprint
        # pprint.pprint(inventory.data)
        return render_template('/dashboard/stocks/inventories/add.html',
                               form=form,
                               stock=stock,
                               items=items)

    return redirect(url_for('dashboard.stocks.view', stock_id=stock.id))
