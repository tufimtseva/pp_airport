from werkzeug.security import generate_password_hash

from model.models import *
from init import app

with app.app_context():
    client1 = Client(name="Khrystyna", surname="Dolynska", country="Ukraine",
                     date_of_birth="2004-03-27", passport_number="FN3378",
                     email="khrystyna.dol@gmail.com",
                     password=generate_password_hash("abcdefg"), role="client")
    client2 = Client(name="Tetiana", surname="Ufimtseva", country="Ukraine",
                     date_of_birth="2004-01-02", passport_number="FN3275",
                     email="t.ufimtseva@gmail.com",
                     password=generate_password_hash("1234567"), role="client")
    manager1 = Client(name="Veronika", surname="Lanchuv", country="Ukraine",
                      date_of_birth="1996-03-27", passport_number="FN3398",
                      email="veronika.lanchuv.kn.2021@lpnu.ua",
                      password=generate_password_hash("lala1"),
                      role='manager')
    manager2 = Client(name="Mary", surname="Queen", country="Ukraine",
                      date_of_birth="1999-03-27", passport_number="FN2398",
                      email="m.queen@gmail.com",
                      password=generate_password_hash("lala2"),
                      role='manager')
    flight1 = Flight(number="3580", departure_city="Lviv",
                     arrival_city="London",
                     departure_time="2022-11-13 19:30:00.016547",
                     arrival_time="2022-11-13 23:45:00.016547", status=1)
    flight2 = Flight(number="2487", departure_city="Berlin",
                     arrival_city="Barcelona",
                     departure_time="2023-11-13 10:00:00.016547",
                     arrival_time="2023-11-13 13:30:00.016547", status=2)

    db.session.add(client1)
    db.session.add(client2)
    db.session.add(manager1)
    db.session.add(manager2)
    db.session.add(flight1)
    db.session.add(flight2)
    db.session.commit()

    booking1 = Booking(reservation_time="2022-10-20 22:03:59.016547",
                       baggage_count=4,
                       flight_id=flight2.id, client_id=client1.id)
    booking2 = Booking(reservation_time="2022-10-28 03:15:34.016547",
                       baggage_count=1,
                       flight_id=flight1.id, client_id=client2.id)

    db.session.add(booking1)
    db.session.add(booking2)
    db.session.commit()

    boarding_check1 = BoardingCheck(type=1, result=1, manager_id=manager1.id,
                                    booking_id=booking1.id)
    boarding_check2 = BoardingCheck(type=1, result=1, manager_id=manager1.id,
                                    booking_id=booking1.id)

    db.session.add(boarding_check1)
    db.session.add(boarding_check2)
    db.session.commit()

    baggage1 = Baggage(weight=8.0, booking_id=client1.id)
    baggage2 = Baggage(weight=5.0, booking_id=client1.id)
    baggage3 = Baggage(weight=3.0, booking_id=client1.id)
    baggage4 = Baggage(weight=3.8, booking_id=client1.id)
    baggage5 = Baggage(weight=2.5, booking_id=client2.id)

    db.session.add(baggage1)
    db.session.add(baggage2)
    db.session.add(baggage3)
    db.session.add(baggage4)
    db.session.add(baggage5)
    db.session.commit()
