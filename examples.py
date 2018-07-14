from aerisweather.aerisweather import AerisWeather
from aerisweather.requests.ParameterType import ParameterType
from aerisweather.requests.RequestLocation import RequestLocation
from aerisweather.requests.RequestAction import RequestAction
from aerisweather.requests.RequestFilter import RequestFilter
# from keys import client_id, client_secret, app_id


aeris = AerisWeather(client_id='j7lOmijllhziSzpk0x6bO',
                     client_secret='a0ZhdOcImgWhhFDEb5X8V64k4WH67lKyGtWTDZe8')

print(aeris)

loc = RequestLocation(postal_code='94086')

obs_list = aeris.observations(location=loc)

print(obs_list)







# forecast_lst = aeris.forecasts(location=loc,
#     params={ParameterType.FORECASTS.FIELDS: 'periods.isDay, periods.maxTempF, periods.minTempF, periods.weather'})

# print("********** \n{}".format(forecast_lst))

# for forecast in forecast_lst:
#     if forecast.periods[0].isDay:
#         day = forecast.periods[0]
#         night = forecast.periods[1]
#     else:
#         day = forecast.periods[1]
#         night = forecast.periods[0]

# print(day)
# print(night)

# print("Today expect " + day.weather + " with a high temp of " + str(day.maxTempF) + "°")
# print("Tonight will be " + night.weather + " with a low temp of " + str(night.minTempF) + "°")