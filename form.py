from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class LoginForm(Form):
    pass


class RegistrationForm(Form):
    '''
    register new user
    '''
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores.')])
    password = PasswordField('Password', validators=[DataRequired(),
                                EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    #make sure email and username don't duplicate
    def validate_email(self, field):
        pass

    def validate_username(self, field):
        pass
