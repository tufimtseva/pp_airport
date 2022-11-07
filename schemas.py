from marshmallow import Schema, fields, validate, validates
from werkzeug.security import generate_password_hash, check_password_hash
class ClientShema(Schema):

    id = fields.Integer()
    name = fields.Str()
    surname = fields.Str()
    country = fields.Str()
    date_of_birth = fields.Date()
    passport_number = fields.Str()
    # password = generate_password_hash(fields.String(validate=validate.Length(min=8)))
    email = fields.Email(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda qqq: generate_password_hash(qqq),
        load_only=True,

    )

# subclass Field
# JSON -> obj = deserialization // hashing
# obj -> JSON = serialization




class ClientAction(Schema):

    id = fields.Integer()
    name = fields.Str()
    surname = fields.Str()
    country = fields.Str()
    date_of_birth = fields.Date()
    passport_number = fields.Str()
    # password = generate_password_hash(fields.String(validate=validate.Length(min=8)))
    email = fields.Email(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda qqq: generate_password_hash(qqq),
        load_only=True,

    )


    # @validates("quantity")
    # def validate_quantity(self, value):
    #     if value < 0:
    #         raise ValidationError("Quantity must be greater than 0.")
    #     if value > 30:
    #         raise ValidationError("Quantity must not be greater than 30.")

class BaggageSchema(Schema):
    id = fields.Integer()
    weight = fields.Float(validate=validate.Range(max=20))
    booking_id = fields.Integer()

class BookingSchema(Schema):
    id = fields.Integer()
    reservation_time = fields.DateTime()
    baggage_count = fields.Integer()
    flight_id = fields.Integer()
    client_id = fields.Integer()

class FlightSchema(Schema):

    id = fields.Integer()
    number = fields.Str()
    departure_city = fields.Str()
    arrival_city = fields.Str()
    departure_time = fields.DateTime()
    arrival_time = fields.DateTime()
    status = fields.Integer()

class ManagerSchema(Schema):

    id = fields.Integer()
    name = fields.Str()
    surname = fields.Str()
    email = fields.Email(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda qqq: generate_password_hash(qqq),
        load_only=True,

    )
    role = fields.Integer()

class BoardingCheckSchema(Schema):
    __tablename__ = 'boarding_check'

    id = fields.Integer()
    type = fields.Integer()
    result = fields.Integer()
    manager_id = fields.Integer()
    booking_id = fields.Integer()
