from . import todo
from app.models import Event, Category
from flask import flash, render_template, jsonify, request, redirect, url_for, json
from flask_login import current_user
from app.todo.forms import EventForm, AddCategoryForm
from datetime import datetime
from flask_login import login_required
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
    form = EventForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).first()
        event = Event(title=form.title.data,
                      category=category.name, completion=form.completion.data,
                      create_time=datetime.utcnow(),
                      sponsor_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        #flash('You have added an new event.')
        return redirect(url_for('todo.index'))
    return render_template('todo/addevent.html', form=form)


@todo.route('/addCategory', methods=['GET', 'POST'])
def addCategory():
    '''
    添加新類別
    :return:
    '''
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('You have added a new category.')
        return redirect(url_for('todo.index'))
    return render_template('todo/addcategory.html', form=form)


@todo.route('/deleteEvent', methods=['POST'])
def deleteEvent():
    data = json.loads(request.form.get('data'))
    eventId = data['id']
    event = Event.query.filter_by(sponsor_id=current_user.id, id = eventId).first()
    db.session.delete(event)
    db.session.commit()
    #flash('You have deleted an event.')
    return jsonify({'result': 'ok'})

@todo.route('/editEvent/', methods=['GET', 'POST'])
@login_required
def editEvent():
    eventId = request.args.get('id')
    event = Event.query.filter_by(sponsor_id=current_user.id, id = eventId).first()
    form = EventForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).first()
        event.title = form.title.data
        event.category = category.name
        event.completion = form.completion.data
        db.session.add(event)
        db.session.commit()
        #flash('You have modified an new event.')
        return redirect(url_for('todo.index'))
    form.title.data = event.title
    form.category.data = event.category
    return render_template('todo/editevent.html', form=form)

@todo.route('/status', methods=['GET', 'POST'])
def status():
    data = json.loads(request.form.get('data'))
    eventId = data['id']
    event = Event.query.filter_by(sponsor_id=current_user.id, id = eventId).first()
    event.completion = data['complete']
    db.session.add(event)
    db.session.commit()
    return jsonify({'result': 'ok'})






