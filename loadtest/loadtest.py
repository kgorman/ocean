from gevent import monkey
monkey.patch_all()

from pymongo import MongoClient, ReadPreference
from pymongo.errors import ConnectionFailure
from datetime import datetime
import random
import signal
import sys
import gevent

try:
    connection = MongoClient('mongodb://options.username:options.password@options.host:options.port/options.db')
    db = connection.[options.db]
    collection = db.ocean_data
except:
    print "unable to connect"
    sys.exit(1)

def get_keys():
    return collection.distinct("station_id")

def hammer(id, key_list):

    key = 0

    while True:
        connection.start_request()
        key = random.choice(key_list)
        val = collection.find({'station_id': key}}).limit(50)
        #print 'greenlet', id, 'got', val
        connection.end_request()

def main():

    key_list = get_keys()
    greenlets = [gevent.spawn(hammer, i, key_list) for i in range(options.threads)]

    def handler():
        gevent.killall(greenlets)
        sys.exit(0)

    gevent.signal(signal.SIGINT, handler)
    gevent.joinall(greenlets)

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--hostname", dest="host", default="127.0.0.1", help="mongodb hostname to connect to")
    parser.add_option("--port", dest="port", type=int, default=27017, help="mongodb port to connect to")
    parser.add_option("--db", dest="db", default="ocean", help="Database to connect to")
    parser.add_option("--username", dest="username", help="username")
    parser.add_option("--password", dest="password", help="password")
    parser.add_option("--threads", dest="threads", type=int, default=10, help="number of threads to spawn")
    (options, args) = parser.parse_args()

    main()
