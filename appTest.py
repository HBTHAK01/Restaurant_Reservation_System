import unittest
from flask import url_for
from app import app

class FlaskTestRoutes(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_sign_up(self):
        tester = app.test_client(self)
        response = tester.get("/sign_up")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_reservation(self):
        tester = app.test_client(self)
        response = tester.get("/reservation")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    

if __name__ == "__main__":
    unittest.main()
