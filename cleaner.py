import pymongo
import bson
from pymongo import MongoClient
import datetime

"""
{
	"_id" : ObjectId("537a3175d211f005ed720a65"),
	"name" : "Port Manatee",
	"lon" : "-82.5621",
	"station_id" : "8726384",
	"products" : [
		{
			"data" : [
				{
					"f" : "0,0,0",
					"t" : "2014-05-19 16:18",
					"v" : 77.2
				}
			],
			"name" : "water_temperature"
		},
		{
			"data" : [
				{
					"f" : "0,0,0",
					"t" : "2014-05-19 16:18",
					"v" : 79.3
				}
			],
			"name" : "air_temperature"
		}
	],
	"lat" : "27.6387",
	"fetch_date" : ISODate("2014-05-19T11:29:40.589Z"),
	"id" : "8726384"
}
"""

client = MongoClient("iad-mongos0.objectrocket.com", 15136)

db = client['ocean']
db.authenticate('kg','kg')
collection = db['ocean_data']

def to_float(value):
  return float(value)

def to_int(value):
  return int(value)

def to_date(value):
  """ format string in format 2014-05-19 16:18 to datetime """
  return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")

def fix_datatypes(doc):
  doc['id'] = to_int(doc['id'])
  doc['lat'] = to_float(doc['lat'])
  doc['lon'] = to_float(doc['lon'])
  for p in doc['products']:
    for d in p['data']:
      if 'v'in d:
        d['v'] = to_float(d['v'])
      if 't' in d and d['t'] != None and type(d['t']) == "String":
        d['t'] = to_date(d['t'])
        print d['t']

  return doc

for doc in collection.find():

  if len(doc['products']) > 0:
    collection.save(fix_datatypes(doc))
    print {"ok":1}
  else:
    print doc['products']
    o = bson.ObjectId(doc['_id'])
    collection.remove({"_id":o})
