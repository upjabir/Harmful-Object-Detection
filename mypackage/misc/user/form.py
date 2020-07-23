from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,PasswordField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
