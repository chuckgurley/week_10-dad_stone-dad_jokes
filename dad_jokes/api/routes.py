from flask import Blueprint, request,jsonify
from dad_jokes.helpers import token_required, random_joke_generator
from dad_jokes.models import db, Dadjoke, dadjoke_schema, dadjokes_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


#Create Drone Endpoint
@api.route('/dadjokes', methods = ["POST"])
@token_required
def create_dadjoke(our_user):
    
    title = request.json['title']
    rating = request.json['rating']  
    joke_setup = request.json['joke_setup']
    punch_line = request.json['punch_line']
    joke_origin = request.json['joke_origin']
    random_joke = random_joke_generator()  
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    dadjoke = Dadjoke(title, rating, joke_setup, punch_line, joke_origin, random_joke, user_token = user_token )

    db.session.add(dadjoke)
    db.session.commit()

    response = dadjokes_schema.dump(Dadjoke)

    return jsonify(response)

#Retrieve(READ) all dadjokes, dadjokes
@api.route('/dadjoke', methods = ['GET'])
@token_required
def get_dadjokes(our_user):
    owner = our_user.token
    Dadjoke = Dadjoke.query.filter_by(user_token = owner).all()
    response = dadjokes_schema.dump(Dadjoke)

    return jsonify(response)

#retrieve one sigular individual lonely dadjoke
#lamedad
@api.route('/dadjokes/<id>', methods = ['GET'])
@token_required
def get_dadjoke(our_user, id):    
    if id:
        dadjokes = Dadjoke.query.get(id)
        response = dadjokes_schema.dump(Dadjoke)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Id equired'}), 401
    
#update dadjoke by id
@api.route('/dadjokes/<id>', methods = ["PUT"])
@token_required
def update_drone(our_user, id): 
    dadjoke = Dadjoke.query.get(id)   
    dadjoke.title = request.json['title']
    dadjoke.rating = request.json['rating']
    dadjoke.joke_setup = request.json['joke_setup']
    dadjoke.punch_line = request.json['punch_line']
    dadjoke.joke_origin = request.json['joke_origin']
    dadjoke.random_joke = random_joke_generator()
    dadjoke.user_token = our_user.token  
     

    db.session.commit()

    response = dadjokes_schema.dump(dadjoke)

    return jsonify(response)

#DELETE dadjoke by id
@api.route('/dadjokes/<id>', methods = ['DELETE'])
@token_required
def delete_dadjokes(our_user, id):
    dadjokes = dadjokes.query.get(id)
    db.session.delete(Dadjoke)
    db.session.commit()

    response = dadjokes_schema.dump(Dadjoke)
    return jsonify(response)
