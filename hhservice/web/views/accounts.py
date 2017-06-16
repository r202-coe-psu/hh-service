from flask import Blueprint, render_template, request

from hhservice.web import forms

module = Blueprint('accounts', __name__)

@module.route('/login')
def login():
    return render_template('accounts/login.html')


@module.route('/register',  methods=('GET', 'POST'))
def register():
    form = forms.accounts.RegisterForm()
    if not form.validate_on_submit():
        return render_template('accounts/register.html',
                               form=form)

    from hhclient import Client
    c = Client(port=5001)
    response = c.users.create(**form.data)
    if response.is_error:
        return render_template('accounts/register.html',
                               form=form,
                               errors=response.errors)

    return render_template('accounts/register_success.html')
