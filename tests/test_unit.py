from unittest import TestCase
from marshmallow import ValidationError
import datetime

from api.schemas import *


class TestPersonSchema(TestCase):
    def test_valid_person(self):
        client = ClientSchema().load({
            "id": 1,
            "name": "User",
            "surname": "User",
            "country": "Ukraine",
            "date_of_birth": "2022-11-23",
            "passport_number": "FN3378",
            "email": "client11@gmail.com",
            "password": "12345",
            "role": "client"
        })
        self.assertEqual(1, client["id"])
        self.assertEqual("User", client["name"])
        self.assertEqual("User", client["surname"])
        self.assertEqual("Ukraine", client["country"])
        self.assertEqual(datetime.date(2022, 11, 23), client["date_of_birth"])
        self.assertEqual("FN3378", client["passport_number"])
        self.assertEqual("client11@gmail.com", client["email"])
        self.assertNotEqual("12345", client["password"])
        self.assertEqual("client", client["role"])

    def test_missing_fields(self):
        with self.assertRaises(ValidationError):
            ClientSchema().load({})

    def test_bad_email(self):
        with self.assertRaises(ValidationError):
            ClientSchema().load({
                "id": 1,
                "name": "User",
                "surname": "User",
                "country": "Ukraine",
                "date_of_birth": "2022-11-23",
                "passport_number": "FN3378",
                "email": "client11",
                "password": "12345",
                "role": "client"
            })

    def test_bad_role(self):
        with self.assertRaises(ValidationError):
            ClientSchema().load({
                "id": 1,
                "name": "User",
                "surname": "User",
                "country": "Ukraine",
                "date_of_birth": "2022-11-23",
                "passport_number": "FN3378",
                "email": "client11@gmail.com",
                "password": "12345",
                "role": "1"
            })

    def test_bad_date(self):
        with self.assertRaises(ValidationError):
            ClientSchema().load({
                "id": 1,
                "name": "User",
                "surname": "User",
                "country": "Ukraine",
                "date_of_birth": "2022.11-23",
                "passport_number": "FN3378",
                "email": "client11@gmail.com",
                "password": "12345",
                "role": "client"
            })


class TestBookingSchema(TestCase):
    def valid_booking(self):

        booking = BookingSchema().load({
            "reservation_time": "2017-07-21T17:32:28.000Z",
            "baggage_count": 2,
            "flight_id": 1,
            "client_id": 1
        })
        self.assertEqual(1, booking["id"])
