from flask import Blueprint, jsonify, request
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


my_blueprint = Blueprint('my_blueprint', __name__)


def error_handler(func):
    def wrapper(*args, **kwargs):
        print("error_handler")
        try:
            res = 0
            if 0 == len(kwargs):
                res = func()
            else:
                res = func(**kwargs)
            #data = res.json()
            if res[1] >= 400:
                return {"code": res[1],"msg":res[0]}, res[1]
            else:
                return res
        except ValidationError as err:
            print(err.messages)
            return {"code": 400, "msg": err.messages}, 400
        except IntegrityError as err:
            print(err.args)
            return {"code": 409,"msg": err.args}, 409

    wrapper.__name__ = func.__name__
    return wrapper;


@app.route('/user', methods=['POST'])
@error_handler
def create_client():
    client_data = ClientShema().load(request.json)
    client = create_entity(Client, **client_data)
    return jsonify(ClientShema().dump(client)), 201


@app.route('/user/<id>', methods=['PUT'])
@error_handler
def update_client(id):
    # try:
    client_data = ClientToUpdateShema().load(request.json)
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return "Client not found", 404
    update_entity(client, **client_data)
    return jsonify(ClientToUpdateShema().dump(client)), 200
    # except IntegrityError as err:
    #     print(err.args)
    #     return {"msg": err.args}, 409
    # except ValidationError as err:
    #     print(err.messages)
    #     return {"msg": err.messages}, 400


@app.route('/user/login', methods=['POST'])
@error_handler
@authBasic.login_required()
def login():
    client = Client.query.filter_by(email=authBasic.current_user()).first()
    if client is None:
        return "There is no user with such email, please register first", 401
    return jsonify(ClientShema().dump(client)), 200


@app.route('/user/logout', methods=['DELETE'])
@error_handler
@authBasic.login_required()
def logout():
    return "", 200


@app.route('/user/<id>', methods=['GET'])
@error_handler
def get_user(id):
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return "There is no user with such id", 404
    return jsonify(ClientShema().dump(client)), 200


@app.route('/baggage', methods=['POST'])
@error_handler
def create_baggage():
    # try:
        baggage_data = BaggageSchema().load(request.json)
        booking_id = baggage_data['booking_id']
        booking = Booking.query.filter_by(id=booking_id).first()
        if booking is None:
            return "There is no booking with such id", 409
        baggage = create_entity(Baggage, **baggage_data)
        return jsonify(BaggageSchema().dump(baggage)), 201
    # except ValidationError as err:
    #     print(err.messages)
    #     return "", 412


@app.route('/baggage/<id>', methods=['GET'])
@error_handler
def get_baggage(id):
    baggage = Baggage.query.filter_by(id=id).first()
    if baggage is None:
        return "There is no baggage with such id", 404
    return jsonify(BaggageSchema().dump(baggage)), 200


@app.route('/booking', methods=['POST'])
@error_handler
def create_booking():
    # try:
        booking_data = BookingSchema().load(request.json)
        client_id = booking_data['client_id']
        flight_id = booking_data['flight_id']
        client = Client.query.filter_by(id=client_id).first()
        if client is None:
            return "There is no client with such id", 409
        flight = Flight.query.filter_by(id=flight_id).first()

        if flight is None:
            return "There is no flight with such id", 409
        booking = create_entity(Booking, **booking_data)
        return jsonify(BookingSchema().dump(booking)), 201
    # except ValidationError as err:
    #     print(err.messages)
    #     return "", 412


@app.route('/booking/<id>', methods=['PUT'])
@error_handler
def update_booking(id):
    # try:
        booking_data = BookingToUpdateSchema().load(request.json)
        booking = Booking.query.filter_by(id=id).first()
        if booking is None:
            return "There is no booking with such id", 404
        update_entity(booking, **booking_data)
        return jsonify(BookingToUpdateSchema().dump(booking)), 200
    # except Exception as error:
    #     print(str(error.orig) + " for parameters" + str(error.params))


@app.route('/booking/<id>', methods=['GET'])
@error_handler
def get_booking(id):
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "There is no booking with such id", 404
    return jsonify(BookingSchema().dump(booking)), 200


@app.route('/booking/<id>', methods=['DELETE'])
@error_handler
def delete_booking(id):
    booking = Booking.query.filter_by(id=id).first()
    baggage = Baggage.query.filter_by(booking_id=id).first()
    boarding_check = BoardingCheck.query.filter_by(booking_id=id).first()
    if baggage is None and boarding_check is None:
        if booking is None:
            return "There is no booking with such id", 404
        delete_entity(booking)
        return "", 200
    else:
        return "Cannot delete booking, the baggage or boarding check already exists", 409


@app.route('/manager/login', methods=['POST'])
@error_handler
@authBasic.login_required()
def login_manager():
    manager = Manager.query.filter_by(email=authBasic.current_user()).first()
    if manager is None:
        return "There is no manager with such email", 401
    return jsonify(ManagerSchema().dump(manager)), 200


@app.route('/manager/logout', methods=['DELETE'])
@error_handler
@authBasic.login_required()
def logout_manager():
    return "", 200


@app.route('/manager/<id>', methods=['GET'])
@error_handler
def get_manager(id):
    manager = Manager.query.filter_by(id=id).first()
    if manager is None:
        return "There is no manager with such email", 404
    return jsonify(ClientShema().dump(manager)), 200


@app.route('/flight/<id>/public-status', methods=['PUT'])
@error_handler
def update_flight_status(id):
    # try:
        # booking_data = request.get_json()
        # status = request.form.get('status', type=int)
        flight_data = FlightToUpdateSchema().load(request.json)
        flight = Flight.query.filter_by(id=id).first()
        if flight is None:
            return "There is no flight with such id", 404
        update_entity(flight, **flight_data)
        return jsonify(FlightToUpdateSchema().dump(flight)), 200
    # except Exception as error:
    #     print(error, " ", error.data)
    #     return "", 412


@app.route('/flight', methods=['GET'])
@error_handler
def get_all_flights():
    return json.dumps([p.as_dict() for p in Flight.query.all()], indent=4, sort_keys=True, default=str), 200


@app.route('/flight/<id>', methods=['GET'])
@error_handler
def get_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "There is no flight with such id", 404
    return jsonify(FlightSchema().dump(flight)), 200


@app.route('/flight/<id>/public-status', methods=['GET'])
@error_handler
def get_flight_status(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "There is no flight with such id", 404
    # return jsonify(flight.status)
    return {"status": flight.status}, 200


@app.route('/flight/<id>/user', methods=['GET'])
@error_handler
def get_users_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "There is no flight with such id", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    clients = []
    for booking in bookings:
        client = Client.query.filter_by(id=booking.client_id).first()
        clients.append(client)
    return json.dumps([p.as_dict() for p in clients], indent=4, sort_keys=True, default=str), 200


@app.route('/flight/<id>/baggage', methods=['GET'])
@error_handler
def get_baggage_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "There is no flight with such id", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    baggages = []
    for booking in bookings:
        baggage = Baggage.query.filter_by(booking_id=booking.id).first()
        if baggage is not None:
            baggages.append(baggage)
    return json.dumps([p.as_dict() for p in baggages], indent=4, sort_keys=True, default=str), 200


@app.route('/boarding-check', methods=['POST'])
@error_handler
def create_boarding_check():

    # try:
    boarding_check_data = BoardingCheckSchema().load(request.json)
    manager_id = boarding_check_data['manager_id']
    booking_id = boarding_check_data['booking_id']
    manager = Manager.query.filter_by(id=manager_id).first()
    booking = Booking.query.filter_by(id=booking_id).first()

    if booking is None or manager is None:
        return "There is no booking or manager with corresponding id", 409
    boarding_check = create_entity(BoardingCheck, **boarding_check_data)
    return jsonify(BoardingCheckSchema().dump(boarding_check)), 200
    # except ValidationError as err:
    #     print(err.messages)
    #     return "", 412


@app.route('/boarding-check', methods=['GET'])
@error_handler
def get_all_boarding_checks():
    return json.dumps([p.as_dict() for p in BoardingCheck.query.all()], indent=4, sort_keys=True, default=str), 200


@app.route('/boarding-check/<id>', methods=['GET'])
@error_handler
def get_boarding_check(id):
    boarding_check = BoardingCheck.query.filter_by(id=id).first()
    if boarding_check is None:
        return "There is no boarding check with corresponding id", 404
    return jsonify(BoardingCheckSchema().dump(boarding_check)), 200


# app.register_blueprint(my_blueprint)

if __name__ == '__main__':
    app.run()
