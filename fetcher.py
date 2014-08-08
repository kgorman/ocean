import requests
import json
import pymongo
import datetime
from pymongo import MongoClient
from optparse import OptionParser

# example url:
# "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20130808 15:00&end_date=20130808 15:06&
# station=8454000&product=water_temperature&units=english&time_zone=gmt&application=ports_screen&format=json"

class Ocean:

    def __init__(self):
        self.connection = MongoClient(options.host,options.port)
        self.database = self.connection[options.db]
        self.database.authenticate(options.username, options.password)

    def noaa_data(self,station_id,product_id):

        baseurl = "http://tidesandcurrents.noaa.gov/api/datagetter?"

        param_date = "date=latest"
        param_time_zone = "time_zone=gmt"
        param_application = "application=kennygorman"
        param_format = "format=json"
        param_units = "units=english"

        param_station = "station="+station_id
        param_product = "product="+product_id

        parameters = [param_product, param_station, param_date, param_time_zone, param_application, param_format, param_units]
        param_url = "&".join(parameters)
        url = "".join([baseurl,param_url])
        try:
            r = requests.get(url)
        except Exception, e:
            print "couldn't fetch url %s" % e

        return json.loads(r.text)

    def to_date(self, value):
      """ format string in format 2014-05-19 16:18 to datetime """
      return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")

    def transform_data(self):
        """ probe API and save document into db """

        products = ['water_temperature','air_temperature','humidity','wind','visibility','air_pressure','salinity']

        all_stations = self.database['stations'].find()

        for station in all_stations:

            station_doc = {}
            station_doc['fetch_date'] = datetime.datetime.now()
            station_doc['station_id'] = station['-ID']
            station_doc['products'] = []

            for product in products:

                # fetch raw data
                station_data = self.noaa_data(station["-ID"], product)

                #{u'data': [{u'f': u'0,0,0', u't': u'2014-07-12 21:00', u'v': u'1015.8'}], u'metadata': {u'lat': u'21.3067', u'lon': u'-157.8670', u'id': u'1612340', u'name': u'Honolulu'}}

                # if it's an error code skip skip and keep processing
                if "error" not in station_data:

                    product_detail = {}

                    # metadata items belong to the station
                    if 'metadata' in station_data:
                        for key in station_data['metadata']:
                            station_doc[key] = station_data['metadata'][key]
                        del station_data['metadata']

                    # data items belong to a product
                    if 'data' in station_data:
                        for key in station_data['data'][0]:
                            if key == 'v':
                                product_detail[key] = float(station_data['data'][0][key])
                            elif key == 't':
                                product_detail[key] = self.to_date(station_data['data'][0][key])
                            else:
                                product_detail[key] = station_data['data'][0][key]

                    # slight denormalization/key naming
                    product_detail['name'] = product
                    station_doc['products'].append(product_detail)

                    station_doc['id'] = int(station_doc['id'])
                    station_doc['station_id'] = int(station_doc['station_id'])
                    # geo is in the form: { loc: { type: "Point", coordinates: [ 40, 5 ] } }
                    station_doc['loc'] = {"type":"Point", "coordinates": [float(station_doc['lon`'], float(station_doc['lat']]}

            if len(station_doc['products']) > 0:
                try:
                    self.database['ocean_data'].save(station_doc)
                    #print station_doc
                except Exception, e:
                    print "Problem inserting: %s" % e

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--hostname", dest="host",help="mongodb hostname to connect to")
    parser.add_option("--port",dest="port",type=int,help="mongodb port to connect to")
    parser.add_option("--db",dest="db",help="Database to connect to")
    parser.add_option("--username",dest="username",help="username")
    parser.add_option("--password",dest="password",help="password")
    (options, args) = parser.parse_args()

    ocean_logger = Ocean()
    ocean_logger.transform_data()
