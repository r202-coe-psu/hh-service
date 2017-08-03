
from wtforms import fields
from wtforms.fields import html5 as html5fields
from wtforms.widgets import html5 as html5widgets
from wtforms import validators

from flask_wtf import FlaskForm

import datetime


class InventoryForm(FlaskForm):
    item = fields.SelectField()
    item_upc = fields.StringField()

    expired_date = html5fields.DateTimeField(
            widget=html5widgets.DateTimeInput(),
            default=datetime.date.today() + datetime.timedelta(days=7))
    # expired_date = html5fields.DateField()
    # expired_time = fields.TextField(widget=html5widgets.TimeInput())

    quantity = fields.IntegerField(
            default=1,
            widget=html5widgets.NumberInput(min=1),
            validators=[validators.NumberRange(min=1)])


class InventoryConsumingForm(FlaskForm):
    item = fields.SelectField()

    consuming_size = fields.IntegerField(
            default=1,
            widget=html5widgets.NumberInput(min=1),
            validators=[validators.NumberRange(min=1)])
