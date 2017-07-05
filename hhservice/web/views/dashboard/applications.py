from flask import Blueprint, render_template, g

module = Blueprint('dashboard.applications',
                   __name__,
                   url_prefix='/applications')


@module.route('/')
@module.route('')
def index():
    c = g.hhclient
    applications = c.applications.list()
    return render_template('/dashboard/applications/index.html',
                           applications=applications)

@module.route('/<app_id>/control/<status>')
def control(app_id):
    if not status or status not in ['active', 'disactive']:
        return redirect(url_for('dashboard.applications.index'))

    c = g.hhclient
    r = c.users.control(app_id, status)
    
    return redirect(url_for('dashboard.applications.index'))
   
