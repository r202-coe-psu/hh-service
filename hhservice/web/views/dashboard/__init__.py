from flask import Blueprint, render_template


url_prefix = '/dashboard'
module = Blueprint('dashboard', __name__, url_prefix=url_prefix)


@module.route('/')
def index():
    return render_template('dashboard/index.html')

