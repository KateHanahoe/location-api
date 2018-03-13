import datetime
from util import apis
from util import flatfile
from util import score


class Location:

    def __init__(self, location_name):

        location_name = location_name.lower()

        # Get saved location details from csv
        location_dict = flatfile.get_saved_details(location_name)
        if location_dict is None:
            raise ValueError("Could not find an entry for '%s'" % location_name)

        # populate location object from saved details
        try:
            self.population = location_dict["population"]
            self.public_transport = location_dict["public_transport"]
            self.temp = location_dict["temperature"]
            self.woeid = location_dict["woeid"]
            self.last_updated = location_dict["last_updated"]
            self.name = location_dict["city"]
            self.weather_desc = location_dict["weather_description"]
            self.country = location_dict["country"]
            self.num_bars = location_dict["bars"]
            self.score = location_dict["score"]
        except KeyError:
            raise

        # Check if saved location details are out of date
        today_datetime = datetime.datetime.now()
        today_str = datetime.datetime.strftime(today_datetime, '%d.%m.%Y')

        if self.last_updated != today_str:
            # update location details where needed
            apis.refresh_weather(self)
            score.calculate(self)
            self.last_updated = today_str

            # save updated details to file
            flatfile.save_details(self)
