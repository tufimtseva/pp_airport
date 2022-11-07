from flask import jsonify, request
from schemas import *
from flask_cors import CORS
# from database.models import app, db, Client, Manager, Flight, Booking, BoardingCheck, Baggage
from utils import *
from marshmallow import Schema, fields, validate, ValidationError
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
app.debug = True

CORS(app)

authBasic = HTTPBasicAuth()

@authBasic.verify_password
def verify_password(email, password):
    print("email: " + email + ", password: " + password)
    return email


# blueprint = BluePrint('api', __name__)


@app.route('/user', methods=['POST'])
def create_client():
    try:
        client_data = ClientAction().load(request.json)
        client = create_entity(Client, **client_data)
        return jsonify(ClientShema().dump(client))
    except ValidationError as err:
        print(err.messages)
        return "", 412

@app.route('/user/<id>', methods=['PUT'])
def update_client(id):
    try:
        client_data = ClientAction().load(request.json)
        client = Client.query.filter_by(id=id).first()
        if client is None:
            return "", 404
        update_entity(client, **client_data)
        return jsonify(ClientShema().dump(client))
    except Exception as error:
            print(str(error.orig) + " for parameters" + str(error.params))
        # id = client_data[id]



@app.route('/user/login', methods=['POST'])
@authBasic.login_required()
def login():
    client = Client.query.filter_by(email=authBasic.current_user()).first()
    if client is None:
        return "", 401
    return jsonify(ClientAction().dump(client))



@app.route('/user/logout', methods=['DELETE'])
@authBasic.login_required()
def logout():
    return "", 200


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return "", 404
    return jsonify(ClientShema().dump(client))


@app.route('/baggage', methods=['POST'])
def create_baggage():
    try:
        baggage_data = BaggageSchema().load(request.json)
        booking_id = baggage_data['booking_id']
        booking = Booking.query.filter_by(id=booking_id).first()
        if booking is None:
            return "", 409
        baggage = create_entity(Baggage, **baggage_data)
        return jsonify(BaggageSchema().dump(baggage))
    except ValidationError as err:
        print(err.messages)
        return "", 412

@app.route('/baggage/<id>', methods=['GET'])
def get_baggage(id):
    baggage = Baggage.query.filter_by(id=id).first()
    if baggage is None:
        return "", 404
    return jsonify(BaggageSchema().dump(baggage))



@app.route('/booking', methods=['POST'])
def create_booking():
    try:
        booking_data = BookingSchema().load(request.json)
        client_id = booking_data['client_id']
        flight_id = booking_data['flight_id']
        client = Client.query.filter_by(id=client_id).first()
        if client is None:
            return "", 401
        flight = Flight.query.filter_by(id=flight_id).first()

        if flight is None:
            return "", 401
        booking = create_entity(Booking, **booking_data)
        return jsonify(BookingSchema().dump(booking))
    except ValidationError as err:
        print(err.messages)
        return "", 412


@app.route('/booking/<id>', methods=['PUT'])
def update_booking(id):
    try:
        booking_data = BookingSchema().load(request.json)
        booking = Booking.query.filter_by(id=id).first()
        if booking is None:
            return "", 404
        update_entity(booking, **booking_data)
        return jsonify(BookingSchema().dump(booking))
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))


@app.route('/booking/<id>', methods=['GET'])
def get_booking(id):
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "", 404
    return jsonify(BookingSchema().dump(booking))

@app.route('/booking/<id>', methods=['DELETE'])
def delete_booking(id):
    booking = Booking.query.filter_by(id=id).first()
    baggage = Baggage.query.filter_by(booking_id=id).first()
    boarding_check = BoardingCheck.query.filter_by(booking_id=id).first()
    if baggage is None and boarding_check is None:
        if booking is None:
            return "", 404
        delete_entity(booking)
        return "", 200
    else:
        return "", 404


@app.route('/manager', methods=['POST'])
def create_manager():
    try:
        manager_data = ManagerSchema().load(request.json)
        manager = create_entity(Client, **manager_data)
        return jsonify(ManagerSchema().dump(manager))
    except ValidationError as err:
        print(err.messages)
        return "", 412


if __name__ == '__main__':
    app.run()
