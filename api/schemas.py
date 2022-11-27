from marshmallow import Schema, fields, validate, validates
from werkzeug.security import generate_password_hash, check_password_hash


class ClientSchema(Schema):

    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    country = fields.Str(required=True)
    date_of_birth = fields.Date(required=True)
    passport_number = fields.Str(validate=validate.Length(equal=6), required=True)
    email = fields.Email(required=True)
    password = fields.Function(
        deserialize=lambda qqq: generate_password_hash(qqq),
        load_only=True, required=True
    )
    role = fields.Str(validate=validate.OneOf(["client", "manager"]), required=True)


class ClientToUpdateSchema(Schema):

    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str()
    surname = fields.Str()
    country = fields.Str()
    date_of_birth = fields.Date()
    passport_number = fields.Str(validate=validate.Length(equal=6))
    email = fields.Email()
    password = fields.Function(
        deserialize=lambda qqq: generate_password_hash(qqq),
        load_only=True

    )
    role = fields.Str(validate=validate.OneOf(["client", "manager"]))


class BaggageSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    weight = fields.Float(validate=validate.Range(min=0, max=20), required=True)
    booking_id = fields.Integer(validate=validate.Range(min=0), required=True)


class BookingSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    reservation_time = fields.DateTime(required=True)
    baggage_count = fields.Integer(validate=validate.Range(min=0), required=True)
    flight_id = fields.Integer(validate=validate.Range(min=0), required=True)
    client_id = fields.Integer(validate=validate.Range(min=0), required=True)


class BookingToUpdateSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    reservation_time = fields.DateTime()
    baggage_count = fields.Integer(validate=validate.Range(min=0))
    flight_id = fields.Integer(validate=validate.Range(min=0))
    client_id = fields.Integer(validate=validate.Range(min=0))


class FlightSchema(Schema):

    id = fields.Integer(validate=validate.Range(min=0))
    number = fields.Str(validate=validate.Regexp("[a-zA-z0-9]*$"), required=True)
    departure_city = fields.Str(required=True)
    arrival_city = fields.Str(required=True)
    departure_time = fields.DateTime(required=True)
    arrival_time = fields.DateTime(required=True)
    status = fields.Integer(validate=validate.OneOf([1, 2, 3, 4]), required=True)


class FlightToUpdateSchema(Schema):

    id = fields.Integer(validate=validate.Range(min=0))
    number = fields.Str(validate=validate.Regexp("[a-zA-z0-9]*$"))
    departure_city = fields.Str()
    arrival_city = fields.Str()
    departure_time = fields.DateTime()
    arrival_time = fields.DateTime()
    status = fields.Integer(validate=validate.OneOf([1, 2, 3, 4]))


class ManagerSchema(Schema):

    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Function(
        deserialize=lambda pas: generate_password_hash(pas),
        load_only=True, required=True
    )
    role = fields.Integer(validate=validate.OneOf([1, 2, 3]), required=True)


class BoardingCheckSchema(Schema):

    id = fields.Integer(validate=validate.Range(min=0))
    type = fields.Integer(validate=validate.OneOf([1, 2, 3]), required=True)
    result = fields.Integer(validate=validate.OneOf([0, 1]), required=True)
    manager_id = fields.Integer(validate=validate.Range(min=0), required=True)
    booking_id = fields.Integer(validate=validate.Range(min=0), required=True)
