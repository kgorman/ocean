import requests
import json
import pymongo
from pymongo import MongoClient
from optparse import OptionParser

# example url:
# "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20130808 15:00&end_date=20130808 15:06&
# station=8454000&product=water_temperature&units=english&time_zone=gmt&application=ports_screen&format=json"

class Ocean:

    def __init__(self):
        pass

    def getData(self):

        baseurl = "http://tidesandcurrents.noaa.gov/api/datagetter?"
        stations = ['8454000']
        products = ['water_temperature','air_temperature','humidity']

        param_date = "date=latest"
        param_time_zone = "time_zone=gmt"
        param_application = "application=ports_screen"
        param_format = "format=json"
        param_units = "units=english"

        connection = MongoClient(options.host,options.port)
        database = connection[options.db]
        database.authenticate(options.username, options.password)

        all_stations = database['stations'].find()

        for station in all_stations:
            for product in products:

                param_station = "station="+station["-ID"]
                param_product = "product="+product

                parameters = [param_product, param_station, param_date, param_time_zone, param_application, param_format, param_units]
                param_url = "&".join(parameters)
                url = baseurl+param_url
                r = requests.get(url)
                data = json.loads(r.text)
                if "error" not in data:
                    database[product].save(json.loads(r.text))

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--hostname", dest="host",help="mongodb hostname to connect to")
    parser.add_option("--port",dest="port",type=int,help="mongodb port to connect to")
    parser.add_option("--db",dest="db",help="Database to connect to")
    parser.add_option("--username",dest="username",help="username")
    parser.add_option("--password",dest="password",help="password")
    (options, args) = parser.parse_args()

    ocean_logger = Ocean()
    ocean_logger.getData()

