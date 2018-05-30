from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Category

class AddEventForm(FlaskForm):
    title = StringField('標題', validators=[DataRequired(), Length(1,64)])
    category = SelectField('類別', coerce=int)
    submit = SubmitField('添加')

    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class AddCategoryForm(FlaskForm):
    name = StringField('類別', validators=[DataRequired()])
    submit = SubmitField('添加')

    def validate_name(self, field):
        if Category.query.filter_by(name = field.data).first:
            raise ValidationError('類別已存在')

class EventForm(FlaskForm):
    pass

class EditEventForm(FlaskForm):
    pass
