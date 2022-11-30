from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
import json


from init import app
from model.models import *
from api.schemas import *
from api.utils import *

auth_basic = HTTPBasicAuth()


@auth_basic.verify_password
def verify_password(email, password):
    user_to_verify = Client.query.filter_by(email=email).first()

    if user_to_verify is None:
        return None
    if check_password_hash(user_to_verify.password, password):
        return user_to_verify
    else:
        return None


@auth_basic.error_handler
def auth_error(status):
    msg = ""
    if status == 401:
        msg = "Wrong email or password"
    if status == 403:
        msg = "Access denied"
    return {"msg": msg, "code": status}, status


def error_handler(controller_func):
    def wrapper(*args, **kwargs):
        try:
            res = 0
            if 0 == len(kwargs):
                res = controller_func()
            else:
                res = controller_func(**kwargs)
            if (res.__class__ == tuple) and res[1] >= 400:
                return {"code": res[1], "msg": res[0]}, res[1]
            else:
                return res
        except ValidationError as err:
            return {"code": 400, "msg": err.messages}, 400
        except IntegrityError as err:
            return {"code": 409, "msg": err.args}, 409

    wrapper.__name__ = controller_func.__name__
    return wrapper


@auth_basic.get_user_roles
def get_user_roles(user):
    return user.role


@app.route('/user', methods=['POST'])
@error_handler
def create_client():
    client_data = ClientSchema().load(request.json)
    client = create_entity(Client, **client_data)
    return jsonify(ClientSchema().dump(client)), 201


@app.route('/user/<id>', methods=['PUT'])
@error_handler
@auth_basic.login_required(role=['client', 'manager'])
def update_client(id):
    current_user = auth_basic.current_user()
    role = current_user.role
    if role == 'client' and current_user.id != int(id):
        return "Access denied", 403
    client_data = ClientToUpdateSchema().load(request.json)
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return "Client not found", 404
    update_entity(client, **client_data)
    return jsonify(ClientToUpdateSchema().dump(client)), 200


@app.route('/user/login', methods=['POST'])
@error_handler
@auth_basic.login_required(role=['client', 'manager'])
def login_user():
    return jsonify(ClientSchema().dump(auth_basic.current_user())), 200


@app.route('/user/<id>', methods=['GET'])
@auth_basic.login_required(role=['client', 'manager'])
@error_handler
def get_user(id):
    current_user = auth_basic.current_user()
    role = current_user.role
    if role == 'client' and current_user.id != int(id):
        return "Access denied", 403
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return "User not found", 404

    return jsonify(ClientSchema().dump(client)), 200


@app.route('/user/<id>', methods=['DELETE'])
@auth_basic.login_required(role=['client', 'manager'])
@error_handler
def delete_user(id):
    current_user = auth_basic.current_user()
    role = current_user.role
    if role == 'client' and current_user.id != int(id):
        return "Access denied", 403
    user_to_delete = Client.query.filter_by(id=id).first()
    if user_to_delete is None:
        return "User not found", 404
    bookings_to_delete = Booking.query.filter_by(client_id=id).all()
    if bookings_to_delete != []:
        for booking in bookings_to_delete:
            baggage_to_delete = Baggage.query\
                .filter_by(booking_id=booking.id).all()
            if baggage_to_delete != []:
                for baggage in baggage_to_delete:
                    delete_entity(baggage)
            boarding_checks_to_delete = BoardingCheck.query\
                .filter_by(booking_id=booking.id).all()
            if boarding_checks_to_delete != []:
                for boarding_check in boarding_checks_to_delete:
                    delete_entity(boarding_check)

        for booking in bookings_to_delete:
            delete_entity(booking)
    delete_entity(user_to_delete)
    return "", 200


@app.route('/baggage', methods=['POST'])
@error_handler
@auth_basic.login_required(role='manager')
def create_baggage():
    baggage_data = BaggageSchema().load(request.json)
    booking_id = baggage_data['booking_id']
    booking = Booking.query.filter_by(id=booking_id).first()
    if booking is None:
        return "There is no booking with such id", 409
    baggage = create_entity(Baggage, **baggage_data)
    return jsonify(BaggageSchema().dump(baggage)), 201


@app.route('/baggage/<id>', methods=['GET'])
@error_handler
@auth_basic.login_required(role='manager')
def get_baggage(id):
    baggage = Baggage.query.filter_by(id=id).first()
    if baggage is None:
        return "Baggage not found", 404
    return jsonify(BaggageSchema().dump(baggage)), 200


@app.route('/booking', methods=['POST'])
@error_handler
@auth_basic.login_required(role='client')
def create_booking():
    current_user = auth_basic.current_user()
    booking_data = BookingSchema().load(request.json)
    client_id = booking_data['client_id']
    flight_id = booking_data['flight_id']
    client = Client.query.filter_by(id=client_id).first()
    if client is None:
        return "There is no client with such id", 409
    if client.id != current_user.id:
        return "Access denied", 403
    flight = Flight.query.filter_by(id=flight_id).first()

    if flight is None:
        return "There is no flight with such id", 409
    booking = create_entity(Booking, **booking_data)
    return jsonify(BookingSchema().dump(booking)), 201


@app.route('/booking/<id>', methods=['PUT'])
@error_handler
@auth_basic.login_required(role='client')
def update_booking(id):
    current_user = auth_basic.current_user()
    booking_data = BookingToUpdateSchema().load(request.json)
    client_id = booking_data['client_id']
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "Booking not found", 404
    if current_user.id != client_id or booking.client_id != current_user.id:
        return "Access denied", 403
    update_entity(booking, **booking_data)
    return jsonify(BookingToUpdateSchema().dump(booking)), 200


@app.route('/booking/<id>', methods=['GET'])
@error_handler
@auth_basic.login_required(role=['client', 'manager'])
def get_booking(id):
    current_user = auth_basic.current_user()
    role = current_user.role
    if role == 'client' and current_user.id != int(id):
        return "Access denied", 403
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "Booking not found", 404
    return jsonify(BookingSchema().dump(booking)), 200


@app.route('/booking/<id>', methods=['DELETE'])
@error_handler
@auth_basic.login_required(role=['client', 'manager'])
def delete_booking(id):
    current_user = auth_basic.current_user()
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "Booking not found", 404
    client_id = booking.client_id
    role = current_user.role
    if role == 'client' and current_user.id != client_id:
        return "Access denied", 403

    baggage = Baggage.query.filter_by(booking_id=id).first()
    boarding_check = BoardingCheck.query.filter_by(booking_id=id).first()
    if baggage is None and boarding_check is None:
        delete_entity(booking)
        return "", 200
    else:
        return "Cannot delete booking, " \
               "the baggage or boarding check already exists", 409


@app.route('/flight', methods=['POST'])
@auth_basic.login_required(role='manager')
@error_handler
def create_flight():
    flight_data = FlightSchema().load(request.json)
    flight = create_entity(Flight, **flight_data)
    return jsonify(FlightSchema().dump(flight)), 201


@app.route('/flight/<id>/public-status', methods=['PUT'])
@error_handler
@auth_basic.login_required(role='manager')
def update_flight_status(id):
    flight_status_data = PublicStatusSchema().load(request.json)
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    update_entity(flight, **flight_status_data)
    return jsonify(FlightToUpdateSchema().dump(flight)), 200


@app.route('/flight/<id>', methods=['PUT'])
@error_handler
@auth_basic.login_required(role='manager')
def update_flight(id):
    flight_data = FlightToUpdateSchema().load(request.json)
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    update_entity(flight, **flight_data)
    return jsonify(FlightToUpdateSchema().dump(flight)), 200


@app.route('/flight', methods=['GET'])
@error_handler
def get_all_flights():
    return json.dumps([p.as_dict() for p in Flight.query.all()],
                      indent=4, sort_keys=True, default=str), 200


@app.route('/flight/<id>', methods=['GET'])
@error_handler
def get_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    return jsonify(FlightSchema().dump(flight)), 200


@app.route('/flight/<id>/public-status', methods=['GET'])
@error_handler
def get_flight_status(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    return {"status": flight.status}, 200


@app.route('/flight/<id>/user', methods=['GET'])
@error_handler
@auth_basic.login_required(role='manager')
def get_users_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    clients = []
    for booking in bookings:
        client = Client.query.filter_by(id=booking.client_id).first()
        clients.append(client)
    return json.dumps([p.as_dict() for p in clients], indent=4,
                      sort_keys=True, default=str), 200


@app.route('/flight/<id>/boarded-user', methods=['GET'])
@error_handler
@auth_basic.login_required(role='manager')
def get_boarded_users_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    clients = []
    for booking in bookings:
        boarding_checks = BoardingCheck.query.filter_by(booking_id=booking.id)\
            .all()
        if boarding_checks != []:
            boarded = True
            for boarding_check in boarding_checks:
                if boarding_check.result == 0:
                    boarded = False
            if boarded:
                client = Client.query.filter_by(id=booking.client_id).first()
                clients.append(client)
    return json.dumps([p.as_dict() for p in clients], indent=4,
                      sort_keys=True, default=str), 200


@app.route('/flight/<id>/baggage', methods=['GET'])
@error_handler
@auth_basic.login_required(role='manager')
def get_baggage_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    baggage = []
    for booking in bookings:
        boarding_checks = BoardingCheck.query.filter_by(
            booking_id=booking.id).all()
        if boarding_checks != []:
            boarded = True
            for boarding_check in boarding_checks:
                if boarding_check.result == 0:
                    boarded = False
            if boarded:
                bagg = Baggage.query.filter_by(booking_id=booking.id).all()
                if bagg != []:
                    baggage.append(bagg)
    return json.dumps([[p.as_dict() for p in bagg] for bagg in baggage],
                      indent=4, sort_keys=True, default=str), 200


@app.route('/flight/<id>/report', methods=['GET'])
@error_handler
@auth_basic.login_required(role='manager')
def get_report_for_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return "Flight not found", 404
    bookings = Booking.query.filter_by(flight_id=id).all()
    clients = []
    baggage = []
    clients_booked = []
    for booking in bookings:
        client = Client.query.filter_by(id=booking.client_id).first()
        clients_booked.append(client)
        boarding_checks = BoardingCheck.query.filter_by(booking_id=booking.id)\
            .all()
        if boarding_checks != []:
            boarded = True
            for boarding_check in boarding_checks:
                if boarding_check.result == 0:
                    boarded = False
            if boarded:
                client = Client.query.filter_by(id=booking.client_id).first()
                clients.append(client)
                bagg = Baggage.query.filter_by(booking_id=booking.id).all()
                if bagg != []:
                    baggage.extend(bagg)
    return {"flight number : ": flight.number,
             "total clients who booked : ": len(clients_booked),
             "total clients who boarded : ": len(clients),
             "total baggage count : ": len(baggage)}


@app.route('/boarding-check', methods=['POST'])
@error_handler
@auth_basic.login_required(role='manager')
def create_boarding_check():
    mgr = auth_basic.current_user()
    boarding_check_data = BoardingCheckSchema().load(request.json)
    manager_id = boarding_check_data['manager_id']
    booking_id = boarding_check_data['booking_id']
    manager = Client.query.filter_by(id=manager_id).first()
    booking = Booking.query.filter_by(id=booking_id).first()
    if booking is None:
        return "There is no booking with corresponding id", 409
    if manager is None:
        return "There is no manager with corresponding id", 409
    if manager.id != mgr.id:
        return "Access denied", 403
    boarding_check = create_entity(BoardingCheck, **boarding_check_data)
    return jsonify(BoardingCheckSchema().dump(boarding_check)), 200


@app.route('/boarding-check', methods=['GET'])
@error_handler
@auth_basic.login_required(role='manager')
def get_all_boarding_checks():
    return json.dumps([p.as_dict() for p in BoardingCheck.query.all()],
                      indent=4, sort_keys=True, default=str), 200


@app.route('/boarding-check/<id>', methods=['GET'])
@error_handler
@auth_basic.login_required(role='manager')
def get_boarding_check(id):
    boarding_check = BoardingCheck.query.filter_by(id=id).first()
    if boarding_check is None:
        return "Boarding check not found", 404
    return jsonify(BoardingCheckSchema().dump(boarding_check)), 200

