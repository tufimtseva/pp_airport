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

authBasic = HTTPBasicAuth()

manager_emails = ['manager1@gmail.com', 'manager2@gmail.com']
# api_blueprint = Blueprint('api', __name__)


@authBasic.verify_password
def verify_password(email, password):
    # print("email: " + email + ", password: " + password)
    user = Client.query.filter_by(email=email).first()
    user_to_verify = Client.query.filter_by(email=email).first()

    if user_to_verify is None:
        # return "There is no user with such email, please register first", 401
        return None
    if check_password_hash(user_to_verify.password, password):
        return user_to_verify
    else:
        return None
        # return {"email : ": client.email}, 200
    # check user.password == password
    # user = Client.query.filter_by(email=user).first()


@authBasic.error_handler
def auth_error(status):
    msg = ""
    if status == 401:
        msg = "Wrong username or password"
    if status == 403:
        msg = "Access denied"
    return {"msg": msg, "code": status}, status


# my_blueprint = Blueprint('my_blueprint', __name__)


def error_handler(func):
    def wrapper(*args, **kwargs):
        # print("error_handler")
        try:
            res = 0
            if 0 == len(kwargs):
                res = func()
            else:
                res = func(**kwargs)
            # data = res.json()
            # res.__class__ != Response
            if (res.__class__ == tuple) and res[1] >= 400:
                return {"code": res[1], "msg": res[0]}, res[1]
            else:
                return res
        except ValidationError as err:
            # print(err.messages)
            return {"code": 400, "msg": err.messages}, 400
        except IntegrityError as err:
            # print(err.args)
            return {"code": 409, "msg": err.args}, 409

    wrapper.__name__ = func.__name__
    return wrapper


@authBasic.get_user_roles
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
@authBasic.login_required(role=['client', 'manager'])
def update_client(id):
    current_user = authBasic.current_user()
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
@authBasic.login_required(role=['client', 'manager'])
def login_user():
    # auth = request.authorization
    # if not auth or not auth.username or not auth.password:
    #     return "There is no username or login  provided", 401
    # client = Client.query.filter_by(email=authBasic.current_user()).first()
    return jsonify(ClientSchema().dump(authBasic.current_user())), 200


# @app.route('/user/logout', methods=['DELETE'])
# @error_handler
# @authBasic.login_required()
# def logout():
#     return "", 200


@app.route('/user/<id>', methods=['GET'])
@authBasic.login_required(role=['client', 'manager'])
@error_handler
def get_user(id):
    current_user = authBasic.current_user()
    role = current_user.role
    if role == 'client' and current_user.id != int(id):
        return "Access denied", 403
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return "There is no user with such id", 404

    return jsonify(ClientSchema().dump(client)), 200

@app.route('/user/<id>', methods=['DELETE'])
@authBasic.login_required(role=['client', 'manager'])
@error_handler
def delete_user(id):
    current_user = authBasic.current_user()
    role = current_user.role
    if role == 'client' and current_user.id != int(id):
        return "Access denied", 403
    user_to_delete = Client.query.filter_by(id=id).first()
    if user_to_delete is None:
        return "There is no user with such id", 404
    bookings_to_delete = Booking.query.filter_by(client_id=id).all()
    if bookings_to_delete != []:
        # baggage_to_delete = []
        # boarding_checks_to_delete = []
        for booking in bookings_to_delete:
            baggage_to_delete = Baggage.query.filter_by(booking_id=booking.id).all()
            if baggage_to_delete != []:
                for baggage in baggage_to_delete:
                    delete_entity(baggage)
            boarding_checks_to_delete = BoardingCheck.query.filter_by(booking_id=booking.id).all()
            if boarding_checks_to_delete != []:
                for boarding_check in boarding_checks_to_delete:
                    delete_entity(boarding_check)

        for booking in bookings_to_delete:
            delete_entity(booking)
    delete_entity(user_to_delete)
    return "", 200



@app.route('/baggage', methods=['POST'])
@error_handler
@authBasic.login_required(role='manager')
def create_baggage():
    # current_email = authBasic.current_user()
    # manager = Manager.query.filter_by(id=id).first()
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
@authBasic.login_required(role='manager')
def get_baggage(id):
    baggage = Baggage.query.filter_by(id=id).first()
    if baggage is None:
        return "There is no baggage with such id", 404
    return jsonify(BaggageSchema().dump(baggage)), 200


@app.route('/booking', methods=['POST'])
@error_handler
@authBasic.login_required(role='client')
def create_booking():
        current_user = authBasic.current_user()
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
    # except ValidationError as err:
    #     print(err.messages)
    #     return "", 412


@app.route('/booking/<id>', methods=['PUT'])
@error_handler
@authBasic.login_required(role='client')
def update_booking(id):
    current_user = authBasic.current_user()
    booking_data = BookingToUpdateSchema().load(request.json)
    client_id = booking_data['client_id']
    # bookings = Booking.query.filter_by(client_id=current_user.id).all()
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "There is no booking with such id", 404
    if current_user.id != client_id or booking.client_id != current_user.id:
        return "Access denied", 403
    update_entity(booking, **booking_data)
    return jsonify(BookingToUpdateSchema().dump(booking)), 200


@app.route('/booking/<id>', methods=['GET'])
@error_handler
@authBasic.login_required(role=['client', 'manager'])
def get_booking(id):
    current_user = authBasic.current_user()
    role = current_user.role
    if role == 'client' and current_user.id != int(id):
        return "Access denied", 403
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "There is no booking with such id", 404
    return jsonify(BookingSchema().dump(booking)), 200


@app.route('/booking/<id>', methods=['DELETE'])
@error_handler
@authBasic.login_required(role=['client', 'manager'])
def delete_booking(id):
    current_user = authBasic.current_user()
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return "There is no booking with such id", 404
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
        return "Cannot delete booking, the baggage or boarding check already exists", 409


# @app.route('/manager/login', methods=['POST'])
# @error_handler
# @authBasic.login_required()
# def login_manager():
#     manager = Manager.query.filter_by(email=authBasic.current_user()).first()
#     if manager is None:
#         return "There is no manager with such email", 401
#     return jsonify(ManagerSchema().dump(manager)), 200


# @app.route('/manager/logout', methods=['DELETE'])
# @error_handler
# @authBasic.login_required()
# def logout_manager():
#     return "", 200


# @app.route('/manager/<id>', methods=['GET'])
# @error_handler
# def get_manager(id):
#     manager = Manager.query.filter_by(id=id).first()
#     if manager is None:
#         return "There is no manager with such email", 404
#     return jsonify(ClientShema().dump(manager)), 200


@app.route('/flight/<id>/public-status', methods=['PUT'])
@error_handler
@authBasic.login_required(role='manager')
def update_flight_status(id):
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
    return {"status": flight.status}, 200


@app.route('/flight/<id>/user', methods=['GET'])
@error_handler
@authBasic.login_required(role='manager')
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
@authBasic.login_required(role='manager')
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
@authBasic.login_required(role='manager')
def create_boarding_check():

    mgr = authBasic.current_user()
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
    # except ValidationError as err:
    #     print(err.messages)
    #     return "", 412


@app.route('/boarding-check', methods=['GET'])
@error_handler
@authBasic.login_required(role='manager')
def get_all_boarding_checks():
    return json.dumps([p.as_dict() for p in BoardingCheck.query.all()], indent=4, sort_keys=True, default=str), 200


@app.route('/boarding-check/<id>', methods=['GET'])
@error_handler
@authBasic.login_required(role='manager')
def get_boarding_check(id):
    boarding_check = BoardingCheck.query.filter_by(id=id).first()
    if boarding_check is None:
        return "There is no boarding check with corresponding id", 404
    return jsonify(BoardingCheckSchema().dump(boarding_check)), 200


# app.register_blueprint(my_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
