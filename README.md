# [Stargaze](https://stargazeseek.com)
Stargaze is a single-page app that helps users find the ideal location and date to look up at the stars. Light pollution, cloud cover, and moonphase are the core factors to consider for an optimal stargazing environment. Stargaze takes in a static NASA satellite image of Earth at night and displays night light data for any given geolocation to infer light pollution. This is combined with weather forecasts for cloud cover and moonphase to determine the optimal stargazing setting. All users can explore the map and visualize night light and weather forecast information. When a user is logged in, they can save specific locations and dates to their personal profile and toggle the map to view all mapped locations versus their personally saved locations.


## Tech Stack
Python, Unittest framework, Flask, PostgreSQL, SQLAlchemy, Geospatial Data Abstraction Library (GDAL), Jinja2, Javascript, JQuery, AJAX, HTML, CSS, Bootstrap, Google Maps and Places API, Dark Sky weather API, NASA API


## Features
* Explore custom map layer created from static NASA satellite image of the earth at night (user account registration not required).

![map](https://image.ibb.co/iCMTFp/sg1.png)

* Get night light measurements and weather forecast (specifically cloudcover and moonphase) for any given geolocation.

![location info](https://image.ibb.co/j9oY89/Screen_Shot_2018_08_15_at_10_35_15_AM.png)

* Register for an account, log in , and save dates and locations of interest to your personal profile.

![user profile](https://image.ibb.co/iaSAvp/sg3.png)


## For Version 2.0
* Improve efficiency of image tile creation, storage, and loading for custom night lights layer.
* Interface with calendar and personal photo APIs to export saved events and link to stargazing photos.