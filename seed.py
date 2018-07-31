
from sqlalchemy import func

from model import db, connect_to_db, Person, Location, SavedRecord, Rating

from server import app

from datetime import datetime

from geopy.geocoders import Nominatim


def load_location(filename):

    for line in open(filename):
        line = line.rstrip().split(' (')

        # print(line[0])
        loc_name = line[0]

        geolocator = Nominatim()
        input_loc = geolocator.geocode(loc_name)
        latlng = str(input_loc.latitude)+','+str(input_loc.longitude)

        # print(latlng)

        loc2 = geolocator.reverse(latlng, language="en")
        lat = loc2.raw['lat']
        lng = loc2.raw['lon']
        country = loc2.raw['address']['country']
        state = loc2.raw['address']['state']
        # city = loc2.raw['address']['city']
        # zipcode = loc2.raw['address']['postcode']

        # print(loc2, lat, lng, country, state)


        location = Location(lat=lat,
                            lng=lng,
                            loc_name=loc_name,
                            country = country,
                            state=state)

        db.session.add(location)
    print("Out of loop")
    db.session.commit()
    print("location db session commit")


def load_person(filename):

    Person.query.delete()

    for line in open(filename):
        email, pw, fname, lname, zipcode = line.rstrip().split(',')

        print(email, pw, fname, lname, zipcode)

        iuser = Person(email=email,
                     password=pw,
                     fname=fname,
                     lname=lname,
                     home_zipcode=zipcode)

        db.session.add(iuser)
        print(iuser)
    db.session.commit()
    print("person db session commit")


def load_saved_record(filename):

    for line in open(filename):
        person_id, loc_id, when_saved, saved_datetime = line.rstrip().split(',')

        print(type(when_saved))
        print(type(saved_datetime))

        dt_when_saved = datetime.fromtimestamp(int(when_saved))
        dt_saved_datetime = datetime.fromtimestamp(int(saved_datetime))

        record = SavedRecord(person_id=int(person_id),
                             loc_id=int(loc_id),
                             when_saved=dt_when_saved,
                             saved_datetime=dt_saved_datetime)

        db.session.add(record)
        
    db.session.commit()
    print("saved record db session commit")


if __name__ == "__main__":
    connect_to_db(app, 'postgresql:///stargazing')
    db.create_all()
    load_location("darksky_sites.txt")
    load_person("user_examples.txt")
    load_saved_record("saved_record_examples.txt")




