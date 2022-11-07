from flask import jsonify, request
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.exc import IntegrityError

from schemas import *
from flask_cors import CORS
# from database.models import app, db, Client, Manager, Flight, Booking, BoardingCheck, Baggage
from utils import *
from marshmallow import Schema, fields, validate, ValidationError
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
app.debug = True
import json
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
        client_data = ClientShema().load(request.json)
        client = create_entity(Client, **client_data)
        return jsonify(ClientShema().dump(client)), 201
    except ValidationError as err:
        print(err.messages)
        return "", 400
    except IntegrityError as err:
        print(err.args)
        return "", 409
@app.route('/user/<id>', methods=['PUT'])
def update_client(id):
    try:
        client_data = ClientShema().load(request.json)
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
    return jsonify(ClientShema().dump(client))



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


@app.route('/manager/login', methods=['POST'])
@authBasic.login_required()
def login_manager():
    manager = Manager.query.filter_by(email=authBasic.current_user()).first()
    if manager is None:
        return "", 401
    return jsonify(ManagerSchema().dump(manager))


@app.route('/manager/logout', methods=['DELETE'])
@authBasic.login_required()
def logout_manager():
    return "", 200

@app.route('/manager/<id>', methods=['GET'])
def get_manager(id):
    manager = Manager.query.filter_by(id=id).first()
    if manager is None:
        return "", 404
    return jsonify(ClientShema().dump(manager))

@app.route('/flight/<id>/setPublicStatus', methods=['PUT'])
def update_flight_status(id):
    try:
       # booking_data = request.get_json()
        #status = request.form.get('status', type=int)
        flight_data = FlightSchema().load(request.json)
        flight = Flight.query.filter_by(id=id).first()
        if flight is None:
            return "", 404
        update_entity(flight, **flight_data)
        return jsonify(FlightSchema().dump(flight))
    except Exception as error:
        print(error, " ", error.data)
        return "", 412

@app.route('/flight/getAll', methods=['GET'])
def get_all_flights():
    return json.dumps([p.as_dict() for p in Flight.query.all()], indent=4, sort_keys=True, default=str)

@app.route('/flight/<id>', methods=['GET'])
def get_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "", 404
    return jsonify(FlightSchema().dump(flight))

@app.route('/flight/<id>/getPublicStatus', methods=['GET'])
def get_flight_status(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "", 404
    # return jsonify(flight.status)
    return { "status": "1" }

@app.route('/flight/<id>/getAllUsers', methods=['GET'])
def get_users_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    clients =[]
    for booking in bookings:
        client = Client.query.filter_by(id=booking.client_id).first()
        clients.append(client)
    return json.dumps([p.as_dict() for p in clients], indent=4, sort_keys=True, default=str)


@app.route('/flight/<id>/getAllBaggage', methods=['GET'])
def get_baggage_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    baggages =[]
    for booking in bookings:
        baggage = Baggage.query.filter_by(booking_id=booking.id).first()
        baggages.append(baggage)
    return json.dumps([p.as_dict() for p in baggages], indent=4, sort_keys=True, default=str)

@app.route('/boarding_check', methods=['POST'])
def create_boarding_check():
    try:
        boarding_check_data = BoardingCheckSchema().load(request.json)
        manager_id = boarding_check_data['manager_id']
        booking_id = boarding_check_data['booking_id']
        manager = Manager.query.filter_by(id=manager_id).first()
        # if manager is None:
        #     return "", 401
        booking = Booking.query.filter_by(id=booking_id).first()

        if booking is None or manager is None:
            return "", 401
        boarding_check = create_entity(BoardingCheck, **boarding_check_data)
        return jsonify(BoardingCheckSchema().dump(boarding_check))
    except ValidationError as err:
        print(err.messages)
        return "", 412


@app.route('/boarding_check/getAll', methods=['GET'])
def get_all_boarding_checks():
    return json.dumps([p.as_dict() for p in BoardingCheck.query.all()], indent=4, sort_keys=True, default=str)

@app.route('/boarding_check/<id>', methods=['GET'])
def get_boarding_check(id):
    boarding_check = BoardingCheck.query.filter_by(id=id).first()
    if boarding_check is None:
        return "", 404
    return jsonify(BoardingCheckSchema().dump(boarding_check))

if __name__ == '__main__':
    app.run()
