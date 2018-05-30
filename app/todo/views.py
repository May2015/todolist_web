from . import todo
from app.models import Event, Category
from flask import flash, render_template, jsonify, request, redirect, url_for
from flask_login import current_user
from app.todo.forms import AddEventForm, AddCategoryForm
from datetime import datetime
from app import db


@todo.route('/index')
def index():
    return render_template('todo/index.html')


@todo.route('/index/jsondata', methods=['GET', 'POST'])
def infos():
    '''
    請求數據謜
    :return:
    '''
    events = Event.query.filter_by(sponsor_id = current_user.id).all()
    if events is None:
        flash('You have not created anything.')
    data = [event.to_json() for event in events]

    return jsonify({'total': len(data), 'rows':data})


@todo.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
    '''
    添加新事件
    :return:
    '''
    form = AddEventForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).first()
        event = Event(title=form.title.data,
                      category=category.name, create_time=datetime.utcnow(),
                      sponsor_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        print('add evenet success.')
        flash('You have added an new event.')
        return redirect(url_for('todo.index'))
    return render_template('todo/addevent.html', form=form)



