from darksky import forecast

sunnyvale = forecast("182208326a8cfd708f594c9b45e646b3", 37.368832, -122.036346)

clouds = [ day["cloudCover"] for day in sunnyvale["daily"]['data'] ]

print(clouds)