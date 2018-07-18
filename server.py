from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, session, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os
import sys
from model import connect_to_db, db, Person, Location, SavedRecord, Rating

from darksky import forecast

from datetime import datetime

from geopy.geocoders import Nominatim

import json
import geojson

from flask_googlemaps import GoogleMaps


app = Flask(__name__)

app.secret_key = "TEST"

app.jinja_env.undefined = StrictUndefined


darksky_key=os.environ['DARKSKY_API_KEY']


@app.route("/")
def index():

    print(session)

    return render_template("homepage.html")


@app.route("/locations")
def show_locations():

    locations = Location.query.all()
    locations_dict = {}

    for location in locations:
        locations_dict[location] = forecast(darksky_key, location.lat, location.lng)


    return render_template("location_list.html",
                           # forecast=forecast,  # pass in forecast module
                           # datetime=datetime,  # pass in datetime module
                           key=darksky_key,            # pass in API key
                           locations_dict=locations_dict)  # pass in location


@app.route("/locations.json")
def location_info():

    loc_lst = Location.query.all()

    feature_lst = []
    for loc in loc_lst:
        lat = loc.lat
        lng = loc.lng
        loc_point = geojson.Point((loc.lng, loc.lat))
        loc_json = geojson.Feature(geometry=loc_point)
        feature_lst.append(loc_json)

    locs_json = geojson.FeatureCollection(feature_lst)


    return jsonify(locs_json)


@app.route('/markercoord', methods=['POST'])
def get_post_javascript_data():
    print(request.form)
    lat = request.form['lat']
    lng = request.form['lng']
    print(lat, lng)


    # coord_lst = coord.split(',')
    # coord_lst = [float(item) for item in coord_lst]
    # print("@@@@@@@@@@@@@@@@@@.{}".format(coord_lst))
    # print("!!!!!!!!!!!!!!!!!!{}".format(type(coord_lst[0])))


    loc = Location(lat=float(lat),
                   lng=float(lng))
    db.session.add(loc)
    db.session.commit()

    # current_loc = db.session.query(Location).filter(Location.lat==coord_lst[0],Location.lng==coord_lst[1]).first()
    # print(current_loc)

    return 'Location saved'

    

@app.route('/save-json', methods=['POST'])
def get_save_data():
    print(request.form)
    print(request.form['lat'], request.form['lng'], request.form['timestamp'])

    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    timestamp = int(request.form['timestamp'])

    print(lat)
    print(lng)

    loc1 = db.session.query(Location).filter(Location.lat < lat+0.0001, Location.lat > lat-0.0001, Location.lng < lng+0.0001, Location.lng > lng-0.0001).first()
    print("**LOC1** {}".format(loc1))

    dt_saved_datetime = datetime.fromtimestamp(timestamp)
    dt_when_saved = datetime.utcnow()

    print("!!Current time!!: {}".format(datetime.utcnow().timestamp()))
    print(dt_saved_datetime)
    print(session['person_id'], type(session['person_id']))

    new_record = SavedRecord(person_id=session['person_id'],
                             loc_id=loc1.loc_id,
                             saved_datetime=dt_saved_datetime,
                             when_saved=dt_when_saved)

    db.session.add(new_record)
    db.session.commit()

    return 'Location saved'


@app.route("/person/<person_id>")
def person_profile(person_id):
    person = db.session.query(Person).get(person_id)
    print(person.saved_records)

    saved_lst = person.saved_records

    return render_template("result.html", saved_lst=saved_lst)



@app.route("/form")
def show_form():
    return render_template("form.html")



@app.route("/userlocation", methods=['POST'])
def get_location_info():


    user_lat = float(request.form.get("lat"))
    user_lng = float(request.form.get("lng"))

    location_dict = forecast(darksky_key, user_lat, user_lng)

    return render_template("result.html", location_dict=location_dict)




@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        passw = request.form["passw"]
        
        login = Person.query.filter(Person.email==email, Person.password==passw).first()
        print(login)
        print(login.password)
        if login is not None:
            session['email'] = email
            session['person_id'] = login.person_id
            flash("Login successful")
            return redirect("/")
        else:
            flash("Email or password incorrect. Try again.")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        passw = request.form['passw']

        register = Person(email = email, password = passw)
        db.session.add(register)
        db.session.commit()
        flash("You've registered. Please login.")

        return redirect("/login")
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('person_id', None)
    flash("You are logged out.")
    return redirect('/')



# GoogleMaps(app, key="")

# @app.route("/test")
# def mapview():
#     # creating a map in the view
#     mymap = Map(
#         identifier="view-side",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[(37.4419, -122.1419)]
#     )
#     sndmap = Map(
#         identifier="sndmap",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
#              'lat': 37.4419,
#              'lng': -122.1419,
#              'infobox': "<b>Hello World</b>"
#           },
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
#              'lat': 37.4300,
#              'lng': -122.1400,
#              'infobox': "<b>Hello World from other place</b>"
#           }
#         ]
#     )
#     return render_template('test.html', mymap=mymap, sndmap=sndmap)






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

