import json
from flask_testing import TestCase
from flask import url_for
import base64

from api.controller import *
from model.models import *
from api.schemas import *
from api.utils import create_entity


class TestApi(TestCase):
    def create_tables(self):
        db.drop_all()
        db.create_all()

    def setUp(self):
        super().setUp()

    def get_basic_client_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"client11@gmail.com:12345").decode("utf8")
        }

    def get_basic_manager_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"manager1@gmail.com:12345").decode("utf8")
        }

    def close_session(self):
        db.session.close()

    def tearDown(self):
        self.close_session()

    def create_app(self):
        return app


class TestAuthentication(TestApi):
    def setUp(self):
        self.create_tables()
        
        self.email = 'client2@gmail.com'
        self.password = "12345"
        self.password_hash = generate_password_hash('12345')
        self.client1_true = {
            "name": "User",
            "surname": "User",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3378",
            "email": "client11@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.client2_true = {
            "name": "User",
            "surname": "User",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3368",
            "email": "client22@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.client_fail_email = {
            "name": "User",
            "surname": "User",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3368",
            "email": "client2@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.client_fail_input = {
            "name": "User",
            "surname": "User1",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3368",
            "email": "client2",
            "password": "12345",
            "role": "client"
        }
        self.client_fail_pass = {
            "name": "User",
            "surname": "User",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3368",
            "email": "client33@gmail.com",
            "password": "1234",
            "role": "client"
        }
        self.manager1_true = {
            "name": "Manager",
            "surname": "Manager",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3368",
            "email": "manager1@gmail.com",
            "password": "12345",
            "role": "manager"
        }
        self.manager2_fail_role = {
            "name": "Manager",
            "surname": "Manager",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3368",
            "email": "manager2@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.baggage1_true = {
            "weight": 18.4,
            "booking_id": 1
        }
        self.booking1_true = {
            "reservation_time": "2017-07-21T17:32:28.000Z",
            "baggage_count": 2,
            "flight_id": 1,
            "client_id": 1
        }
        self.booking_fail_client = {
            "reservation_time": "2017-07-21T17:32:28.000Z",
            "baggage_count": 2,
            "flight_id": 1,
            "client_id": 2
        }
        self.boarding_check1_true = {
            "type": 1,
            "result": 1,
            "manager_id": 1,
            "booking_id": 1
        }
        self.boarding_check_fail_manager = {
            "type": 1,
            "result": 1,
            "manager_id": 2,
            "booking_id": 1
        }
        self.boarding_check_fail_role = {
            "type": 1,
            "result": 1,
            "manager_id": 2,
            "booking_id": 1
        }
        self.flight1_true = {
            "number": "35246",
            "departure_city": "Lviv",
            "arrival_city": "Paris",
            "departure_time": "2023-11-13 10:00:00.00",
            "arrival_time": "2023-11-13 15:00:00.00",
            "status": 1
        }

    def test_authenticate_success(self):
        client_data = ClientSchema().load(self.client1_true)
        # client_to_add = create_entity(Client, **client_data)
        client_to_add = Client(**client_data)
        db.session.add(client_to_add)
        db.session.commit()
        resp = self.client.post(url_for("login_user"), headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json["email"], "client11@gmail.com")

    def test_authenticate_fail_email(self):
        client_data = ClientSchema().load(self.client_fail_email)
        client_to_add = create_entity(Client, **client_data)
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("login_user"), headers=headers)
        self.assertEqual(401, resp.status_code)

    def test_authenticate_fail_password(self):
        client_data = ClientSchema().load(self.client_fail_pass)
        client_to_add = create_entity(Client, **client_data)
        resp = self.client.post(url_for("login_user"), headers=self.get_basic_client_headers())
        self.assertEqual(401, resp.status_code)

    def test_create_client(self):
        payload = json.dumps(
            self.client1_true
        )
        resp = self.client.post(url_for("create_client"), headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_create_client_fail_email(self):
        client_data_add = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data_add)
        payload = json.dumps(
            self.client1_true
        )
        resp = self.client.post(url_for("create_client"), headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(409, resp.status_code)

    def test_create_client_fail_input(self):
        payload = json.dumps(
            self.client_fail_input
        )
        resp = self.client.post(url_for("create_client"), headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(400, resp.status_code)

    def test_update_client(self):
        # client_data_add = ClientSchema().load(self.client1_true)
        # client_to_add = create_entity(Client, **client_data_add)
        client_data_update = ClientSchema().load(self.client1_true)
        client_to_update = create_entity(Client, **client_data_update)
        payload = json.dumps(
            self.client1_true
        )
        headers = self.get_basic_client_headers()  # header can be also with manager credentials
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_client", id=client_to_update.id),
                               headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_client_access_denied(self):
        client_data_update = ClientSchema().load(self.client1_true)
        client_to_update = create_entity(Client, **client_data_update)
        payload = json.dumps(
            self.client1_true
        )
        headers = self.get_basic_client_headers()  # header can be also with manager credentials
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_client", id=2),
                               headers=headers, data=payload)
        self.assertEqual(403, resp.status_code)

    def test_update_client_not_found(self):
        payload = json.dumps(
            self.client1_true
        )
        headers = self.get_basic_client_headers()  # header can be also with manager credentials
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_client", id=1),
                               headers=headers, data=payload)
        self.assertEqual(401, resp.status_code)

    def test_get_user(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        resp = self.client.get(url_for("get_user", id=client_to_add.id), headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_user_access_denied(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        resp = self.client.get(url_for("get_user", id=2), headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_delete_user(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        baggage_data = BaggageSchema().load(self.baggage1_true)
        baggage_to_add = create_entity(Baggage, **baggage_data)
        boarding_check_data = BoardingCheckSchema().load(self.boarding_check1_true)
        boarding_check_to_add = create_entity(BoardingCheck, **boarding_check_data)
        resp = self.client.delete(url_for("delete_user", id=client_to_add.id),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_delete_user_access_denied(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        client_data = ClientSchema().load(self.client2_true)
        client_to_add2 = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        baggage_data = BaggageSchema().load(self.baggage1_true)
        baggage_to_add = create_entity(Baggage, **baggage_data)
        boarding_check_data = BoardingCheckSchema().load(self.boarding_check1_true)
        boarding_check_to_add = create_entity(BoardingCheck, **boarding_check_data)
        resp = self.client.delete(url_for("delete_user", id=client_to_add2.id),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_delete_user_not_found(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        baggage_data = BaggageSchema().load(self.baggage1_true)
        baggage_to_add = create_entity(Baggage, **baggage_data)
        boarding_check_data = BoardingCheckSchema().load(self.boarding_check1_true)
        boarding_check_to_add = create_entity(BoardingCheck, **boarding_check_data)
        resp = self.client.delete(url_for("delete_user", id=5),
                                  headers=self.get_basic_manager_headers())
        self.assertEqual(404, resp.status_code)

    def test_create_baggage(self):
        payload = json.dumps(
            self.baggage1_true
        )
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_baggage"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_create_baggage_no_booking(self):
        payload = json.dumps(
            self.baggage1_true
        )
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)

        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_baggage"), headers=headers, data=payload)
        self.assertEqual(409, resp.status_code)

    def test_get_baggage(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        baggage_data = BaggageSchema().load(self.baggage1_true)
        baggage_to_add = create_entity(Baggage, **baggage_data)

        payload = json.dumps(
            self.baggage1_true
        )
        resp = self.client.get(url_for("get_baggage", id=baggage_to_add.id),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_baggage_no_baggage(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        baggage_data = BaggageSchema().load(self.baggage1_true)
        baggage_to_add = create_entity(Baggage, **baggage_data)

        payload = json.dumps(
            self.baggage1_true
        )
        resp = self.client.get(url_for("get_baggage", id=2),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(404, resp.status_code)

    def test_create_booking(self):
        payload = json.dumps(
            self.booking1_true
        )
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_booking"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_create_booking_no_flight(self):
        payload = json.dumps(
            self.booking1_true
        )
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        # flight_data = FlightSchema().load(self.flight1_true)
        # flight_to_add = create_entity(Flight, **flight_data)
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_booking"), headers=headers, data=payload)
        self.assertEqual(409, resp.status_code)

    def test_create_booking_no_client(self):
        payload = json.dumps(
            self.booking_fail_client
        )
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_booking"), headers=headers, data=payload)
        self.assertEqual(409, resp.status_code)

    def test_create_booking_access_denied(self):
        payload = json.dumps(
            self.booking1_true
        )
        client_data_2 = ClientSchema().load(self.client2_true)
        client_to_add_2 = create_entity(Client, **client_data_2)
        client_data_1 = ClientSchema().load(self.client1_true)
        client_to_add_1 = create_entity(Client, **client_data_1)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_booking"), headers=headers, data=payload)
        self.assertEqual(403, resp.status_code)

    def test_update_booking(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        payload = json.dumps(
            self.booking1_true
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_booking", id=booking_to_add.id), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_booking_access_denied(self):
        client_data_2 = ClientSchema().load(self.client2_true)
        client_to_add_2 = create_entity(Client, **client_data_2)
        client_data_1 = ClientSchema().load(self.client1_true)
        client_to_add_1 = create_entity(Client, **client_data_1)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        payload = json.dumps(
            self.booking1_true
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_booking", id=booking_to_add.id), headers=headers, data=payload)
        self.assertEqual(403, resp.status_code)

    def test_get_booking(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        resp = self.client.get(url_for("get_booking", id=booking_to_add.id),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_booking_access_denied(self):
        client_data_2 = ClientSchema().load(self.client2_true)
        client_to_add_2 = create_entity(Client, **client_data_2)
        client_data_1 = ClientSchema().load(self.client1_true)
        client_to_add_1 = create_entity(Client, **client_data_1)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        resp = self.client.get(url_for("get_booking", id=booking_to_add.id),
                               headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_delete_booking(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        resp = self.client.delete(url_for("delete_booking", id=booking_to_add.id),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_delete_booking_no_id(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        # booking_data = BookingSchema().load(self.booking1_true)
        # booking_to_add = create_entity(Booking, **booking_data)

        headers = self.get_basic_client_headers()

        resp = self.client.delete(url_for("delete_booking", id=1),
                               headers=self.get_basic_client_headers())
        self.assertEqual(404, resp.status_code)

    def test_delete_booking_with_baggage(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        baggage_data = BaggageSchema().load(self.baggage1_true)
        baggage_to_add = create_entity(Baggage, **baggage_data)

        resp = self.client.delete(url_for("delete_booking", id=booking_to_add.id),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(409, resp.status_code)

    def test_delete_booking_access_denied(self):
        client_data_2 = ClientSchema().load(self.client2_true)
        client_to_add_2 = create_entity(Client, **client_data_2)
        client_data_1 = ClientSchema().load(self.client1_true)
        client_to_add_1 = create_entity(Client, **client_data_1)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        resp = self.client.delete(url_for("delete_booking", id=booking_to_add.id),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_update_flight_status(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)

        payload = json.dumps(
            self.flight1_true
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_flight_status", id=flight_to_add.id), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_get_flight_status(self):
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)

        resp = self.client.get(url_for("get_flight_status", id=flight_to_add.id))
        self.assertEqual(200, resp.status_code)

    def test_get_flight_status_fail(self):
        resp = self.client.get(url_for("get_flight_status", id=1))
        self.assertEqual(404, resp.status_code)
        self.assertEqual({'code': 404, 'msg': 'There is no flight with such id'}, resp.json)

    def test_get_flight(self):
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)

        resp = self.client.get(url_for("get_flight", id=flight_to_add.id))
        self.assertEqual(200, resp.status_code)

    def test_get_flight_no_flight(self):
        resp = self.client.get(url_for("get_flight", id=1))
        self.assertEqual(404, resp.status_code)

    def test_get_all_flights(self):
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        resp = self.client.get(url_for("get_all_flights"))
        self.assertEqual(200, resp.status_code)

    def test_get_users_for_flight(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)

        resp = self.client.get(url_for("get_users_for_flight", id=flight_to_add.id),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_baggage_for_flight(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)

        resp = self.client.get(url_for("get_baggage_for_flight", id=flight_to_add.id),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_create_boarding_check(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        payload = json.dumps(
            self.boarding_check1_true
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_boarding_check"), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_create_boarding_check_no_booking(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)

        payload = json.dumps(
            self.boarding_check1_true
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_boarding_check"), headers=headers, data=payload)
        self.assertEqual(409, resp.status_code)

    def test_create_boarding_check_no_manager(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        payload = json.dumps(
            self.boarding_check_fail_manager
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_boarding_check"), headers=headers, data=payload)
        self.assertEqual(409, resp.status_code)

    def test_create_boarding_check_access_denied(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        client_data = ClientSchema().load(self.manager2_fail_role)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)

        payload = json.dumps(
            self.boarding_check_fail_role
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("create_boarding_check"), headers=headers, data=payload)
        self.assertEqual(403, resp.status_code)

    def test_get_all_boarding_checks(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        boarding_check_data = BoardingCheckSchema().load(self.boarding_check1_true)
        boarding_check_to_add = create_entity(BoardingCheck, **boarding_check_data)

        resp = self.client.get(url_for("get_all_boarding_checks"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_all_boarding_checks_fail(self):
        client_data = ClientSchema().load(self.client1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        boarding_check_data = BoardingCheckSchema().load(self.boarding_check1_true)
        boarding_check_to_add = create_entity(BoardingCheck, **boarding_check_data)

        resp = self.client.get(url_for("get_all_boarding_checks"),
                               headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_get_boarding_check(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        boarding_check_data = BoardingCheckSchema().load(self.boarding_check1_true)
        boarding_check_to_add = create_entity(BoardingCheck, **boarding_check_data)

        resp = self.client.get(url_for("get_boarding_check", id=boarding_check_to_add.id),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_boarding_check_fail_id(self):
        client_data = ClientSchema().load(self.manager1_true)
        client_to_add = create_entity(Client, **client_data)
        flight_data = FlightSchema().load(self.flight1_true)
        flight_to_add = create_entity(Flight, **flight_data)
        booking_data = BookingSchema().load(self.booking1_true)
        booking_to_add = create_entity(Booking, **booking_data)
        boarding_check_data = BoardingCheckSchema().load(self.boarding_check1_true)
        boarding_check_to_add = create_entity(BoardingCheck, **boarding_check_data)

        resp = self.client.get(url_for("get_boarding_check", id=2),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(404, resp.status_code)
