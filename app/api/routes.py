from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, cars_schema, car_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'hello': 'world'}

# Creating car
@api.route('/car', methods = ['POST'])
@token_required
def add_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, year, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Retrieving all cars
@api.route('/car', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Retrieving specific car
@api.route('/car/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# Update car
@api.route('/car/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Deleting car
@api.route('/car/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
