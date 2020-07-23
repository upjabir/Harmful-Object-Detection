from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
   


class SignUpForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Sign up')