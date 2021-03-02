from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Name',[DataRequired()])
    email = StringField('Email',[Email(message=('Not a valid email address.')),DataRequired()])
    subject = StringField('Subject',[DataRequired()])
    body = TextField('Message',[DataRequired(),Length(min=4,message=('Your message is too short.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
