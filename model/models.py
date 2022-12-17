from init import db


class User(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250))
    role = db.Column(db.String(50))

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    departure_city = db.Column(db.String(50), nullable=False)
    arrival_city = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.DateTime(timezone=True))
    arrival_time = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    reservation_time = db.Column(db.DateTime(timezone=True))
    baggage_count = db.Column(db.Integer, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))


class BoardingCheck(db.Model):
    __tablename__ = 'boarding_check'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Baggage(db.Model):
    __tablename__ = 'baggage'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}
