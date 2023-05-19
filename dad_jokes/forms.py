from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
     
    username = StringField('Username', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired()])
    password = PasswordField('Password', validators= [DataRequired()])
    submit_button = SubmitField()
    
class Dadjokeform(FlaskForm):
    
    title = StringField('title')
    rating = StringField('rating')  
    joke_setup = StringField('joke_setup')
    punch_line = StringField('punch_line')
    joke_origin = StringField('joke_origin')
    submit_button = SubmitField()
    
    
    
    
