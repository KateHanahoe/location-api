from tornado.web import RequestHandler
from http import HTTPStatus
import json
import location
import csv
import tornado.httpclient
import socket


class LocationHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        """
        Retrieve information about a city.
        :param args:
        :param kwargs:
        :return:
        """

        # retrieve city name from URL
        url_components = [x for x in self.request.path.split("/") if x]
        city_name = url_components[-1]

        # create a location object for the specified city
        try:
            city = location.Location(city_name)
            response = {'city_name': city.name,
                        'current_temperature': city.temp,
                        'current_weather_description': city.weather_desc,
                        'population': city.population,
                        'bars': city.num_bars,
                        'public_transport': city.public_transport,
                        'city_score': city.score}
            self.set_status(HTTPStatus.OK)
            self.write(json.dumps(response))
        except(
            csv.Error,
            tornado.httpclient.HTTPError,
            socket.gaierror,
            TypeError,
            IndexError,
            KeyError,
            ValueError
        ):
            response = {'error': 'Unable to retrieve details for your specified city.'}
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.write(json.dumps(response))
