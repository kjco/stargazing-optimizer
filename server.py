from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, session, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os
import sys
from model import connect_to_db, db, Person, Location, SavedRecord, Rating

from darksky import forecast

from datetime import datetime

from geopy.geocoders import Nominatim

import geojson

from flask_googlemaps import GoogleMaps


app = Flask(__name__)

app.secret_key = "TEST"

app.jinja_env.undefined = StrictUndefined


darksky_key=os.environ['DARKSKY_API_KEY']


@app.route("/")
def index():

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
    coord = request.form['coord_data']
    coord_lst = coord.split(',')
    coord_lst = [float(item) for item in coord_lst]
    print("@@@@@@@@@@@@@@@@@@.{}".format(coord_lst))
    print("!!!!!!!!!!!!!!!!!!{}".format(type(coord_lst[0])))


    loc = Location(lat=coord_lst[0],
                   lng=coord_lst[1])
    db.session.add(loc)
    db.session.commit()

    current_loc = db.session.query(Location).filter(Location.lat==coord_lst[0],Location.lng==coord_lst[1]).first()
    print(current_loc)

    return coord

    



@app.route("/form")
def show_form():
    return render_template("form.html")



@app.route("/userlocation", methods=['POST'])
def get_location_info():


    user_lat = float(request.form.get("lat"))
    user_lng = float(request.form.get("lng"))

    location_dict = forecast(darksky_key, user_lat, user_lng)

    return render_template("result.html", location_dict=location_dict)




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

