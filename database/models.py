from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:leisuregurube@localhost:5432/Airport"

db = SQLAlchemy(app)



class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250))

    def __repr__(self):
        return "<User: '{}' '{}', email: '{}'>" \
            .format(self.name, self.surname, self.email)
    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}



class Manager(db.Model):
    __tablename__ = 'manager'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250))
    role = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Manager: '{}' '{}', email: '{}', role: '{}'>" \
            .format(self.name, self.surname, self.email, self.role)


class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    departure_city = db.Column(db.String(50), nullable=False)
    arrival_city = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.DateTime(timezone=True))
    arrival_time = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return "<Flight  '{}' - '{}' on '{}' - '{}'>" \
            .format(self.departure_city, self.arrival_city, self.departure_time, self.arrival_time)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}



class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    reservation_time = db.Column(db.DateTime(timezone=True))
    baggage_count = db.Column(db.Integer, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
        return "<Booking by user id: '{}' >" \
            .format(self.client_id)


class BoardingCheck(db.Model):
    __tablename__ = 'boarding_check'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    def __repr__(self):
        return "<Boarding result '{}' for booking id: '{}' >" \
            .format(self.result, self.booking_id)
    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Baggage(db.Model):
    __tablename__ = 'baggage'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    def __repr__(self):
        return "<Baggage weight: '{}' >" \
            .format(self.weight)
    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


@app.route('/')
def home():
    return 'Home page '


@app.route('/api/v1/hello-world-<val>')
def hello_world(val):
    return 'Hello World ' + val, 200


if __name__ == '__main__':
    app.run(debug=True)
