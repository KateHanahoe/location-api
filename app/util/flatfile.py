import csv

""" Methods for reading and writing location data to and from a csv file """
FLAT_FILE = "data/european_cities.csv"


def get_saved_details(location_name):
    try:
        with open(FLAT_FILE) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['city'] == location_name.lower():
                    return row
    except (OSError, csv.Error):
        # csv file cannot be opened or a problem was encountered when attempting to process the file
        raise


def save_details(location_obj):

    try:
        with open(FLAT_FILE) as inf:
            reader = csv.DictReader(inf.readlines())

        with open(FLAT_FILE, 'w') as outf:
            writer = csv.DictWriter(outf, reader.fieldnames)
            writer.writeheader()
            for row in reader:
                if row['city'] == location_obj.name:
                    writer.writerow(location_to_dict(location_obj))
                    break
                else:
                    writer.writerow(row)
            writer.writerows(reader)
    except (OSError, csv.Error):
        # csv file cannot be opened or a problem was encountered when attempting to process the file
        raise


def location_to_dict(location_obj):
    location_dict = {
        'population': location_obj.population,
        'public_transport': location_obj.public_transport,
        'temperature': location_obj.temp,
        'woeid': location_obj.woeid,
        'last_updated': location_obj.last_updated,
        'city': location_obj.name,
        'weather_description': location_obj.weather_desc,
        'country': location_obj.country,
        'bars': location_obj.num_bars,
        'score': location_obj.score
    }
    return location_dict
