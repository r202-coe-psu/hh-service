from flask import Blueprint, render_template, request

from hhservice.web import forms

module = Blueprint('accounts', __name__)

@module.route('/login')
def login():
    return render_template('accounts/login.html')


@module.route('/register')
def register():
    form = forms.accounts.RegisterForm(request.args)
    return render_template('accounts/register.html',
            form=form)
