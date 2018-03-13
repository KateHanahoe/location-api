""" Logic for determining a location's score based on its other, predefined properties """


def calculate(location_obj):
    """ Primary method for calculating score, calls subsequent methods """
    # The current logic for calculating a location's score is not very sophisticated...
    # every scoring criteria is first converted into a number between 1 and 10 (some don't need to be converted)
    # there is a method in this module to handle each of these conversions where necessary
    # the overall score, calculated within this method, is simply the average of each criteria

    temp_score = get_temp_score(location_obj.temp)

    weather_desc_score = get_weather_desc_score(location_obj.weather_desc)

    num_bars_score = get_num_bars_score(location_obj.num_bars)

    public_transport_score = int(location_obj.public_transport)

    criteria = [temp_score, weather_desc_score, num_bars_score, public_transport_score]

    location_obj.score = float(sum(criteria)) / max(len(criteria), 1)


def get_temp_score(temp):
    """ Rate given temperature (Celsius) from 1-10, any temperature between 23 and 27 gets a score of 10 """
    if 13 <= temp < 18:
        return 2
    elif 18 <= temp < 23:
        return 6
    elif 23 <= temp < 28:
        return 10
    elif 28 <= temp < 33:
        return 6
    elif 33 <= temp < 38:
        return 2
    else:
        return 0


def get_weather_desc_score(weather_desc):
    """ Rate given weather description from 1-10 """
    # Weather descriptions are retrieved from an API and there are only 10 possible values
    # the following weather descriptions get a score of zero by default:
    # Snow, Sleet, Hail, Thunderstorm, Heavy Cloud, Heavy Rain
    if weather_desc == "Light Rain":
        return 2
    elif weather_desc == "Showers":
        return 3
    elif weather_desc == "Light Cloud":
        return 5
    elif weather_desc == "Clear":
        return 10
    else:
        return 0


def get_num_bars_score(num_bars):
    """ Convert the number of bars in a city into a number from 1-10, more bars = higher score """
    # The number of bars is rounded to the nearest 100th and then divided by 10
    # this formula consistently returns a value between 0 and 10, any exception is simply reduced to 10
    bar_score = int(round(int(num_bars), -2) / 100)
    if bar_score > 10:
        bar_score = 10
    return bar_score
