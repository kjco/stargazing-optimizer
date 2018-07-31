from unittest import TestCase
from server import app
from model import connect_to_db, db
from seed import load_location, load_person, load_saved_record
from flask import session
import json


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and seed with data
        db.create_all()
        load_location('locations_fortest.txt')
        load_person('user_examples.txt')
        load_saved_record('records_fortest.txt')

        def _mock_get_locations_dict(loc_lst):
            mock_dict = {}
            mock_forecast = open('mock_forecast_response.txt', 'r').read()
            mock_forecast = json.loads(mock_forecast)

            for loc in loc_lst:
                mock_dict[loc] = mock_forecast

            return mock_dict

        import server
        server.get_locations_dict = _mock_get_locations_dict


    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Show my weather", result.data)


    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "test1@email.com", "passw": "test123"},
                                  follow_redirects=True)
        # print(result.data)
        self.assertIn(b"Click to show saved records", result.data)


    def test_register(self):
        """Test register route"""

        result = self.client.post("/register",
                                  data={"email": "register_test@test.com", "passw":"register123"},
                                  follow_redirects=True)

        self.assertIn(b"Login", result.data)
        self.assertNotIn(b">Register</button>", result.data)


    def test_locations(self):
        """Test rendering of locations page."""

        result = self.client.get("/locations")
        self.assertIn(b"<th>1532720982</th>", result.data)








if __name__ == "__main__":
    import unittest

    unittest.main()
