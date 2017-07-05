from flask import Blueprint, render_template, g, url_for, redirect, session
from flask_login import login_user, logout_user, login_required, current_user

from hhservice.web import forms
from hhservice.web.acl import User

module = Blueprint('accounts', __name__)


@module.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = forms.accounts.LoginForm()

    if not form.validate_on_submit():
        return render_template('accounts/login.html',
                               form=form)

    name = form.name.data
    password = form.password.data
    c = g.hhclient
    auth = c.authenticate(name=name, password=password)
    if auth.is_error:
        return render_template('accounts/login.html',
                               form=form,
                               errors=auth.errors)

    print('--->', auth.data)
    user = c.users.get(auth.data['user']['id'])
    buildings = c.buildings.list()

    session['token'] = auth.data
    session['user'] = user.data
    session['buildings'] = [building.data for building in buildings]

    user = User(**user.data)

    login_user(user)

    return redirect(url_for('dashboard.index'))


@module.route("/logout")
@login_required
def logout():
    session.pop('token', None)
    session.pop('user', None)
    session.pop('buildings', None)
    logout_user()
    return redirect(url_for('site.index'))


@module.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.accounts.RegisterForm()
    if not form.validate_on_submit():
        return render_template('accounts/register.html',
                               form=form)

    c = g.hhclient

    response = c.users.create(**form.data)
    if response.is_error:
        return render_template('accounts/register.html',
                               form=form,
                               errors=response.errors)

    return render_template('accounts/register_success.html')
