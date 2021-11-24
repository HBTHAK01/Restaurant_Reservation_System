import unittest
from flask import url_for
from app import app

class FlaskTestRoutes(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/", follow_redirects=True)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_sign_up(self):
        tester = app.test_client(self)
        response = tester.get("/sign_up", follow_redirects=True)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_reservation(self):
        tester = app.test_client(self)
        response = tester.get("/reservation", follow_redirects=True)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
class FlaskTestHTMLdata(unittest.TestCase):
    def test_login_form(self):
        tester = app.test_client(self)
        response = tester.get("/")
        #gets html page in text form
        html = response.get_data(as_text=True)
        # make sure all the fields are included
        assert 'name = "email_login"' in html
        assert 'name = "pass_login"' in html

    def test_sign_up_form(self):
        tester = app.test_client(self)
        response = tester.get("/sign_up")
        #gets html page in text form
        html = response.get_data(as_text=True)
        # make sure all the fields are included
        assert 'name = "fname"' in html
        assert 'name = "lname"' in html
        assert 'name = "contact"' in html
        assert 'name = "email"' in html
        assert 'name = "pass_word"' in html
        assert 'name = "pass_c"' in html
        

if __name__ == "__main__":
    unittest.main()
