from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

#adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#import secrets module (from python) generates a token for each user
import secrets

#import flask login to check for an authenticated user and store current user
from flask_login import UserMixin, LoginManager

#import flask marshmallow to help create our Schemas 
from flask_marshmallow import Marshmallow 

db = SQLAlchemy() 
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin): 
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    dadjoke = db.relationship('Dadjoke', backref = 'owner', lazy = True)
    
    def __init__(self, email, username, first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.username = username
        self.token = self.set_token(24)
        
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the Mailer!"
        

class Dadjoke(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(150))
    rating = db.Column(db.String(50))   
    joke_setup = db.Column(db.String(300))
    punch_line = db.Column(db.String(300))
    joke_origin = db.Column(db.String(150))       
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
    
    def __init__(self, title, rating, joke_setup, punch_line, joke_origin, user_token):
        self.id = self.set_id()
        self.title = title
        self.rating = rating        
        self.joke_setup = joke_setup
        self.punch_line = punch_line
        self.joke_origin = joke_origin
        self.user_token = user_token
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Dad Joke {self.title} has been added to the Joke Bucket!"

class Dadjokeschema(ma.Schema):
    class Meta:
        fields =['id', 'title', 'rating', 'joke_setup', 'punch_line', 'joke_origin' ,'user_token' ]     
        
    
dadjoke_schema = Dadjokeschema()  
dadjokes_schema = Dadjokeschema(many = True)  