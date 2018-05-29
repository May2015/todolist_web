from . import todo
from app.models import Event
from flask import flash, render_template
from flask_login import current_user

@todo.route('/index')
def index():
    events = Event.query.filter_by(sponsor_id = current_user.id).all()
    if events is None:
        flash('You have not created anything.')
    return render_template('todo/index.html', events=events)