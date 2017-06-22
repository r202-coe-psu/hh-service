from flask import Blueprint, render_template
from flask_login import login_required

url_prefix = '/dashboard'
module = Blueprint('dashboard', __name__, url_prefix=url_prefix)


def register_blueprint(app):
    app.register_blueprint(module)

@module.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')

