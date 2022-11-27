from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
# # from sqlalchemy.sql import func
from sqlalchemy.orm import Session, sessionmaker, scoped_session, declarative_base, backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5432/Airport"

db = SQLAlchemy(app)

engine = create_engine("postgresql://postgres:12345@localhost:5432/Airport")
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

Base = declarative_base()
Base.query = db.session.query_property()


class Client(Base):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250))
    role = db.Column(db.String(250))

    # def __repr__(self):
    #     return "<User: '{}' '{}', email: '{}'>" \
    #         .format(self.name, self.surname, self.email)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}

    def get_roles(self):
        return "client"


# class Manager(db.Model):
#     __tablename__ = 'manager'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     surname = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(250))
#     role = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return "<Manager: '{}' '{}', email: '{}', role: '{}'>" \
#             .format(self.name, self.surname, self.email, self.role)


class Flight(Base):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    departure_city = db.Column(db.String(50), nullable=False)
    arrival_city = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.DateTime(timezone=True))
    arrival_time = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.Integer, nullable=False)

    # def __repr__(self):
    #     return "<Flight  '{}' - '{}' on '{}' - '{}'>" \
    #         .format(self.departure_city, self.arrival_city, self.departure_time, self.arrival_time)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Booking(Base):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    reservation_time = db.Column(db.DateTime(timezone=True))
    baggage_count = db.Column(db.Integer, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    # def __repr__(self):
    #     return "<Booking by user id: '{}' >" \
    #         .format(self.client_id)


class BoardingCheck(Base):
    __tablename__ = 'boarding_check'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    # def __repr__(self):
    #     return "<Boarding result '{}' for booking id: '{}' >" \
    #         .format(self.result, self.booking_id)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Baggage(Base):
    __tablename__ = 'baggage'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    # def __repr__(self):
    #     return "<Baggage weight: '{}' >" \
    #         .format(self.weight)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}
