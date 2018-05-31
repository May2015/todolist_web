from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Category

# 編輯新增事件共用一個form
class EventForm(FlaskForm):
    title = StringField('標題', validators=[DataRequired(), Length(1,64)])
    category = SelectField('類別', coerce=int)
    completion = BooleanField('是否完成',  default=False)
    submit = SubmitField('添加')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class AddCategoryForm(FlaskForm):
    name = StringField('類別', validators=[DataRequired()])
    submit = SubmitField('添加')

    def validate_name(self, field):
        if Category.query.filter_by(name = field.data).first():
            raise ValidationError('類別已存在')


