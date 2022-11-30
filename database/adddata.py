from werkzeug.security import generate_password_hash

from model.models import *
from init import app

with app.app_context():
    client1 = Client(name="Khrystyna", surname="Dolynska", country="Ukraine",
                     date_of_birth="2004-03-27", passport_number="FN3378",
                     email="khrystyna.dol@gmail.com",
                     password=generate_password_hash("12345"), role="client")
    client2 = Client(name="Tetiana", surname="Ufimtseva", country="Ukraine",
                     date_of_birth="2004-01-02", passport_number="FN3255",
                     email="t.ufimtseva@gmail.com",
                     password=generate_password_hash("54321"), role="client")
    client3 = Client(name="Oleksii", surname="Vasilenko", country="Ukraine",
                     date_of_birth="2001-02-04", passport_number="FN2125",
                     email="o.vasilenko@gmail.com",
                     password=generate_password_hash("54321"), role="client")
    client4 = Client(name="Valeria", surname="Voronych", country="Ukraine",
                     date_of_birth="2002-10-14", passport_number="FN2120",
                     email="v.voronych@gmail.com",
                     password=generate_password_hash("54321"), role="client")
    manager1 = Client(name="Veronika", surname="Lanchuv", country="Ukraine",
                      date_of_birth="1996-03-27", passport_number="FN3198",
                      email="veronika.lanchuv.kn.2021@lpnu.ua",
                      password=generate_password_hash("m1"),
                      role='manager')
    manager2 = Client(name="Mary", surname="Queen", country="Ukraine",
                      date_of_birth="1999-03-27", passport_number="FN2328",
                      email="m.queen@gmail.com",
                      password=generate_password_hash("m2"),
                      role='manager')
    manager3 = Client(name="Anastasia", surname="Shepilenko", country="Ukraine",
                      date_of_birth="1986-06-20", passport_number="FN3098",
                      email="nastya.shep.kn.2021@lpnu.ua",
                      password=generate_password_hash("m3"),
                      role='manager')
    flight1 = Flight(number="LCY3580", departure_city="Lviv",
                     arrival_city="London",
                     departure_time="2022-11-13 19:30:00.016547",
                     arrival_time="2022-11-13 23:45:00.016547", status=1)
    flight2 = Flight(number="BCN2487", departure_city="Berlin",
                     arrival_city="Barcelona",
                     departure_time="2023-11-13 10:00:00.016547",
                     arrival_time="2023-11-13 13:30:00.016547", status=2)

    db.session.add(client1)
    db.session.add(client2)
    db.session.add(client3)
    db.session.add(client4)
    db.session.add(manager1)
    db.session.add(manager2)
    db.session.add(manager3)
    db.session.add(flight1)
    db.session.add(flight2)
    db.session.commit()

    booking1 = Booking(reservation_time="2022-10-20 22:03:59.016547",
                       baggage_count=2,
                       flight_id=flight1.id, client_id=client1.id)
    booking2 = Booking(reservation_time="2022-10-28 03:15:34.016547",
                       baggage_count=3,
                       flight_id=flight2.id, client_id=client2.id)
    booking3 = Booking(reservation_time="2022-10-28 03:15:34.016547",
                       baggage_count=1,
                       flight_id=flight2.id, client_id=client3.id)
    booking4 = Booking(reservation_time="2022-10-28 03:15:34.016547",
                       baggage_count=0,
                       flight_id=flight2.id, client_id=client4.id)

    db.session.add(booking1)
    db.session.add(booking2)
    db.session.add(booking3)
    db.session.add(booking4)
    db.session.commit()

    boarding_check1 = BoardingCheck(type=1, result=1, manager_id=manager1.id,
                                    booking_id=booking1.id)
    boarding_check2 = BoardingCheck(type=2, result=1, manager_id=manager2.id,
                                    booking_id=booking1.id)
    boarding_check3 = BoardingCheck(type=3, result=1, manager_id=manager3.id,
                                    booking_id=booking1.id)
    boarding_check4 = BoardingCheck(type=1, result=1, manager_id=manager1.id,
                                    booking_id=booking2.id)
    boarding_check5 = BoardingCheck(type=2, result=0, manager_id=manager2.id,
                                    booking_id=booking2.id)
    boarding_check6 = BoardingCheck(type=3, result=1, manager_id=manager3.id,
                                    booking_id=booking2.id)
    boarding_check7 = BoardingCheck(type=1, result=1, manager_id=manager1.id,
                                    booking_id=booking3.id)
    boarding_check8 = BoardingCheck(type=2, result=1, manager_id=manager2.id,
                                    booking_id=booking3.id)
    boarding_check9 = BoardingCheck(type=3, result=1, manager_id=manager3.id,
                                    booking_id=booking3.id)
    boarding_check10 = BoardingCheck(type=1, result=1, manager_id=manager1.id,
                                    booking_id=booking4.id)
    boarding_check11 = BoardingCheck(type=2, result=1, manager_id=manager2.id,
                                    booking_id=booking4.id)
    boarding_check12 = BoardingCheck(type=3, result=1, manager_id=manager3.id,
                                    booking_id=booking4.id)

    db.session.add(boarding_check1)
    db.session.add(boarding_check2)
    db.session.add(boarding_check3)
    db.session.add(boarding_check4)
    db.session.add(boarding_check5)
    db.session.add(boarding_check6)
    db.session.add(boarding_check7)
    db.session.add(boarding_check8)
    db.session.add(boarding_check9)
    db.session.add(boarding_check10)
    db.session.add(boarding_check11)
    db.session.add(boarding_check12)
    db.session.commit()

    baggage1 = Baggage(weight=18.0, booking_id=booking1.id)
    baggage2 = Baggage(weight=5.0, booking_id=booking1.id)
    baggage3 = Baggage(weight=19.0, booking_id=booking2.id)
    baggage4 = Baggage(weight=13.8, booking_id=booking2.id)
    baggage5 = Baggage(weight=12.5, booking_id=booking2.id)
    baggage6 = Baggage(weight=10.5, booking_id=booking3.id)

    db.session.add(baggage1)
    db.session.add(baggage2)
    db.session.add(baggage3)
    db.session.add(baggage4)
    db.session.add(baggage5)
    db.session.add(baggage6)
    db.session.commit()
