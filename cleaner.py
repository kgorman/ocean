import pymongo
from pymongo import MongoClient

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
collection = db['testme']

def convert_to_float(doc):
  for p in doc['products']:
    index = 0
    for d in p['data']:
      if 'v'in d:
        index += 1
        value = float(d['v'])
        d['v'] = value
  return doc

for doc in collection.find():
  print convert_to_float(doc)
  collection.save(convert_to_float(doc))
