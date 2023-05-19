from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from dad_jokes.forms import Dadjokeform
from dad_jokes.models import Dadjoke, db

from dad_jokes.helpers import random_joke_generator 

site = Blueprint('site', __name__, template_folder = 'site_templates')



@site.route('/')
def home():
    print("what do you know")
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    Dadform = Dadjokeform()

    try:
        if request.method == "POST" and Dadform.validate_on_submit():
            title = Dadform.title.data
            rating = Dadform.rating.data
            joke_setup = Dadform.joke_setup.data
            punch_line = Dadform.punch_line.data
            joke_origin = Dadform.joke_origin.data            
            user_token = current_user.token
            
            dadjokes = Dadjoke(title, rating, joke_setup, punch_line, joke_origin, user_token)

            db.session.add(dadjokes)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception("Joke not created, please check your form and try again!")
    
    current_user_token = current_user.token

    dadjokes = Dadjoke.query.filter_by(user_token=current_user_token)

    cool_phrase = "KACHEWWW"

    
    return render_template('profile.html', form=Dadform, dadjokes = dadjokes, cool_phrase = cool_phrase )