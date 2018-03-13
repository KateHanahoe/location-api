from tornado.web import RequestHandler
from http import HTTPStatus
import json
import location
import csv
import tornado.httpclient
import socket


class LocationComparisonHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        """
        Retrieves information about multiple cities, rates them and returns a ranking and score for each city.
        :param args:
        :param kwargs:
        :return:
        """

        # retrieve URL "cities" param
        city_names = args[0].split(",")

        # check that more than one city has been specified
        if(len(city_names) == 1):
            response = {'error': 'At least two cities must be specified.'}
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.write(json.dumps(response))

        else:
            found_cities = []
            not_found = []

            # attempt to source data for each city
            for city_name in city_names:
                try:
                    city = location.Location(city_name)
                    found_cities.append({'city_name': city.name, 'city_score': city.score})
                except(
                    csv.Error,
                    tornado.httpclient.HTTPError,
                    socket.gaierror,
                    TypeError,
                    IndexError,
                    KeyError,
                    ValueError
                ):
                    not_found.append(city_name)

            # if all cities are found, compare them
            if len(found_cities) == len(city_names):
                response = self.compare(found_cities)
                self.set_status(HTTPStatus.OK)
                self.write(json.dumps(response))

            # if one or more cities have not been found, let the user know which ones
            elif len(found_cities) > 0:
                response = {'error': 'Unable to retrieve details for the following cities: ' + (' ,'.join(not_found))}
                self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.write(json.dumps(response))

            else:
                response = {'error': 'Unable to retrieve details for any of the cities specified.'}
                self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.write(json.dumps(response))

    def compare(self, found_cities):
        """ compare and rank cities against each other """
        # Returns a list of dictionaries, each dictionary corresponds to a city
        sorted_list = sorted(found_cities, key=lambda k: k['city_score'], reverse=True)
        for index, city in enumerate(sorted_list):
            city['city_rank'] = (index+1)
        return {'city_data': sorted_list}
