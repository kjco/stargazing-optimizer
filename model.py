"""Data model and functions for Star Gazing optimizer project"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Person(db.Model):
    """Person (user) of stargazing optimizer site"""

    __tablename__ = "person"

    person_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64), nullable=True)
    lname = db.Column(db.String(64), nullable=True)
    home_zipcode = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide representation when object printed."""

        return "<Person person_id={} email={} home_zipcode={}>".format(
                                                            self.person_id,
                                                            self.email,
                                                            self.home_zipcode)


class Location(db.Model):

    __tablename__ = "location"

    loc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    loc_name = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.String(64))
    state = db.Column(db.String(64))
    country = db.Column(db.String(64))

    def __repr__(self):
        return "<Location loc_id={} lat={} lng={} loc_name={}>".format(
            self.loc_id, self.lat, self.lng, self.loc_name)


class SavedRecord(db.Model):
    """saved locations and times by persons"""

    __tablename__ = "saved_record"

    saved_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.person_id"),
                        nullable=False)
    loc_id = db.Column(db.Integer, db.ForeignKey("location.loc_id"),
                       nullable=False)
    saved_datetime = db.Column(db.DateTime, nullable=False)
    when_saved = db.Column(db.DateTime, nullable=False)

    # Establish relationship to Person table; backref is "saved_records"
    person = db.relationship("Person", backref=db.backref("saved_records",
                                                      order_by=saved_id))

    # Establish relationship to Location table; backref is "saved_records"
    location = db.relationship("Location", backref=db.backref("saved_records"),
                               order_by=saved_id)

    # Establish relationship to rating table (should be 1:1);
    # backref is "saved_record"
    rating = db.relationship("Rating", backref="saved_record")

    def __repr__(self):
        return "<SavedRecord saved_id={} person_id={} loc_id={} saved_datetime={}>".format(
            self.saved_id, self.person_id, self.loc_id, self.saved_datetime)


class Rating(db.Model):

    __tablename__ = "rating"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    saved_id = db.Column(db.Integer, db.ForeignKey("saved_record.saved_id"))
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Rating rating_id={} saved_id={} score={}>".format(
                self.rating_id, self.saved_id, self.score)






# Helper function

def connect_to_db(app, db_uri):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


