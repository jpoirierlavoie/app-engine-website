from flask_wtf import FlaskForm
from wtforms import StringField, TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    name = StringField('Name',[DataRequired()])
    email = StringField('Email',[Email(message=('Not a valid email address.')),DataRequired()])
    body = TextField('Message',[DataRequired(),Length(min=4,message=('Your message is too short.'))])
    submit = SubmitField('Send')
