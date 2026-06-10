import json
import unittest
from unittest.mock import patch

from vindecodervehicle import VinDecoderClient
from vindecodervehicle.exceptions import ApiError, AuthenticationError, InvalidArgumentError
from vindecodervehicle.http import HttpClient


class MockHttpClient(HttpClient):
    def __init__(self):
        super().__init__()
        self.responses: list[tuple[int, str]] = []

    def queue(self, status: int, payload: dict) -> None:
        self.responses.append((status, json.dumps(payload)))

    def get(self, url: str, params: dict) -> tuple[int, str]:
        return self.responses.pop(0)


class VinDecoderClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.http = MockHttpClient()
        self.client = VinDecoderClient("demo-user", "demo-key", http_client=self.http)

    def test_decode_vin(self) -> None:
        self.http.queue(200, {
            "success": True,
            "timestamp": "2025-07-02T22:37:25+00:00",
            "api_version": "2.0",
            "data": {
                "carId": 55565,
                "vin": "",
                "make": "BMW",
                "model": "3 Coupe (E92)",
                "year": "2007",
                "yearEnd": "2013",
                "description": "316 i",
                "body": "Coupe",
                "fuel": "Petrol",
                "engine": "Petrol Engine",
                "cubicCapacityCcm": 1599,
                "cubicCapacityLiters": 1.6,
                "powerHpFrom": 122,
                "powerHpTo": 122,
                "kwPowerFrom": "",
                "kwPowerTo": 90,
                "cylinder": 4,
                "drive": "Rear Wheel Drive",
                "valves": 4,
                "fuelMixtureFormation": "Direct Injection",
                "aspiration": "",
                "cylinderDesign": "",
                "coolingType": "",
                "tonnage": "",
                "axleLoadFromKg": "",
                "axleLoadToKg": "",
                "axleStyle": "",
                "axleType": "",
                "axleBody": "",
                "axleConfiguration": "",
                "wheelMounting": "",
                "brakeType": "",
                "hmdMfrModelName": "",
            },
        })

        vehicle = self.client.decode_vin("WF0GXXGAJ69C71882")
        self.assertEqual(vehicle.car_id, 55565)
        self.assertEqual(vehicle.make, "BMW")
        self.assertEqual(vehicle.full_name, "BMW 3 Coupe (E92) 316 i")

    def test_list_brands(self) -> None:
        self.http.queue(200, {
            "success": True,
            "timestamp": "2025-07-02T22:55:17+00:00",
            "api_version": "2.0",
            "data": [
                {"name": "BMW", "slug": "bmw"},
                {"name": "AUDI", "slug": "audi"},
            ],
        })

        brands = self.client.list_brands()
        self.assertEqual(len(brands), 2)
        self.assertEqual(brands[0].slug, "bmw")

    def test_invalid_vin(self) -> None:
        with self.assertRaises(InvalidArgumentError):
            self.client.decode_vin("ABC")

    def test_authentication_error(self) -> None:
        self.http.queue(401, {"success": False, "message": "Invalid credentials"})
        with self.assertRaises(AuthenticationError):
            self.client.list_brands()

    def test_api_error(self) -> None:
        self.http.queue(200, {"success": False, "message": "Quota exceeded"})
        with self.assertRaises(ApiError):
            self.client.list_brands()


if __name__ == "__main__":
    unittest.main()