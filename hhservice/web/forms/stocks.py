
from wtforms import fields
from wtforms import validators

from flask_wtf import FlaskForm

from .fields import TagListField


class InventoryForm(FlaskForm):
    name = fields.TextField('Name', validators=[validators.InputRequired()])
    description = fields.TextField('Description')
    tags = TagListField('Tags')
