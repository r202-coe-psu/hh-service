from flask import Blueprint, render_template


module = Blueprint('accounts', __name__)


@module.route('/login')
def login():
    return render_template('accounts/login.html')


@module.route('/register')
def register():
    return render_template('accounts/register.html')
