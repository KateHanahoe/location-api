import tornado.httpclient
import json
import socket

""" Methods for connecting to 3rd party APIs to update location data """


def refresh_weather(location_obj):
    """ Connect to Meta Weather API to retrieve up-to-date weather information """

    try:
        url = 'https://www.metaweather.com/api/location/' + str(location_obj.woeid) + '/'
        request = tornado.httpclient.HTTPRequest(url, 'GET')
        client = tornado.httpclient.HTTPClient()
        response = client.fetch(request)
        response_obj = json.loads(response.body.decode())
        client.close()
    except (tornado.httpclient.HTTPError, socket.gaierror):
        # HTTPError is raised for non-200 responses
        # gaierror indicates a DNS problem (do you need to specify a proxy?)
        raise

    try:
        location_obj.weather_desc = response_obj["consolidated_weather"][0]["weather_state_name"]
        temp = response_obj["consolidated_weather"][0]["the_temp"]
        location_obj.temp = int(round(temp))
    except (TypeError, IndexError, KeyError):
        # problem with response object
        raise
    return
