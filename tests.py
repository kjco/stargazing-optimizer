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

        app.config['SECRET_KEY'] ='key'

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

        def _mock_get_location_geojson(loc_lst):

            geojson_str = """{ "features": [ { "geometry": 
                { "coordinates": [ -100.00, 100.00 ], "type": "Point" }, 
                "properties": { "id": 1, "name": "StarsEverywhere", "light": 1 }, 
                "type": "Feature" }], "type" : "FeatureCollection"}"""

            return geojson_str


        import server
        server.get_locations_dict = _mock_get_locations_dict
        server.get_location_geojson = _mock_get_location_geojson


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


    def test_login_incorrect(self):
        result = self.client.post("/login",
                                  data={"email": "wrongemail", "passw": "na"},
                                  follow_redirects=True)
        self.assertIn(b"Email or password incorrect. Try again.", result.data)
        self.assertNotIn(b"Click to show saved records", result.data)


    def test_register(self):
        """Test register route"""

        result = self.client.post("/register",
                                  data={"email": "register_test@test.com", "passw":"register123"},
                                  follow_redirects=True)

        self.assertIn(b"Login", result.data)
        self.assertNotIn(b">Register</button>", result.data)

    def test_register_render(self):

        result = self.client.get('/register')
        self.assertIn(b"""<button type="submit" class="btn form-control btn-primary">Register</button>""",
            result.data)


    def test_locations(self):
        """Test rendering of locations page."""

        result = self.client.get("/locations")
        self.assertIn(b"<th>1532720982</th>", result.data)


    def test_lightinfo(self):

        result = self.client.post("/lightinfo",
            data={"lat": "33.9269162252255", "lng": "-118.107039343964"},
            follow_redirects=True)
        self.assertIn(b"254", result.data)


    def test_get_post_javascript_data(self):

        result = self.client.post("/markercoord",
            data={"lat": "33.9269162252255", "lng": "-118.107039343964", "name": "AwesomeLocation"},
            follow_redirects=True)
        self.assertIn(b"New Location Saved", result.data)


    def test_location_info(self):

        result = self.client.get("/locations.json")
        self.assertIn(b"StarsEverywhere", result.data)



class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        app.config['SECRET_KEY'] ='key'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and seed with data
        db.create_all()
        load_location('locations_fortest.txt')
        load_person('user_examples.txt')
        load_saved_record('records_fortest.txt')

        def _mock_get_geojson(locs_lst):

            geojson_str = """{ "features": [ { "geometry": 
            { "coordinates": [ -100.00, 100.00 ], "type": "Point" }, 
            "properties": { "loc_id": 1, "name": "Awesome Park", "saved_id": 1, "timestamp": 10000 }, 
            "type": "Feature" }], "type" : "FeatureCollection"}"""

            return geojson_str


        import server
        server.get_geojson = _mock_get_geojson


        with self.client as c:
            with c.session_transaction() as sess:
                sess['person_id'] = 1


    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    def test_saved_records_info(self):

        result = self.client.get("/myrecords.json")
        self.assertIn(b"Awesome Park", result.data)


    def test_get_save_data(self):

        result = self.client.post("/save-json",
            data={"lat": "33.09553545", "lng": "-116.301897714978", "timestamp": "1531337675"},
            follow_redirects=True)

        self.assertIn(b"Location saved", result.data)


    def test_get_loc_rating(self):

        result = self.client.post("/rating-json",data={"score": 5, "saved_id":1}, follow_redirects=True)
        self.assertIn(b"Thank you for rating this location!", result.data)





if __name__ == "__main__":
    import unittest

    unittest.main()
