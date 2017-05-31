from flask import Blueprint, render_template, request

from hhservice.web import forms

module = Blueprint('accounts', __name__)

@module.route('/login')
def login():
    return render_template('accounts/login.html')


@module.route('/register',  methods=('GET', 'POST'))
def register():
    form = forms.accounts.RegisterForm()
    if form.validate_on_submit():
        return 'ok'
    else:
        return render_template('accounts/register.html',
                form=form)
