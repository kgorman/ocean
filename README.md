## Ocean

### Overview
Ocean exists to populate a sample MongoDB dataset with NOAA data for usage in examples, teaching, etc.  This dataset is naturally suited for MongoDB and thus a perfect candidate.  The data is pulled from the API and normalized slightly to ensure easy queryability.

This dataset has some nice native properties
- Density.  Fetching all 'products' is a single document fetch and likely 3 I/O's max.
- Shardability.  Sharding on station_id (HASHED) works really nicely.
- Geo.  Lat/Lon index for doing any geo queries.

The data is pulled via http://tidesandcurrents.noaa.gov/api/

NOAA has been collecting this data for 150 years. This data is open and paid for by the US Taxpayer. CO-OPS is the authoritative source for accurate, reliable, and timely water-level and current measurements that support safe and efficient maritime commerce, sound coastal management, and recreation.

http://tidesandcurrents.noaa.gov/about.html
http://co-ops.nos.noaa.gov/publications/CO-OPS_Measurement_SpecUpdated_4.pdf

### Installation

This is a stand alone python script.  You need a MongoDB to store this data. ObjectRocket works nicely to shard things out. You will need to install the stations background metadata first.

Requirements:
- requests
- pymongo

1) Setup background metadata using mongoimport:
```
gunzip stations.json.gz
mongoimport --host=<hostname> --port=<port> --username=<username> --password=<password> --db=<mydb> --collection=stations stations.json
```

2) Run the script via the command line like:
```
python fetcher.py
```

Or perhaps run it in cron every 20 minutes.  Data is cataloged over time and nicely suited to graphing, mapping, heatmaps, etc.
```
0,20,40 * * * * $HOME/ocean/run_fetcher.sh > /tmp/fetcher.out
```

A sample document looks like:

```
{
	"_id" : ObjectId("53e4fcc42239c23dce3cb7bc"),
	"station_id" : 8461490,
	"loc" : {
		"type" : "Point",
		"coordinates" : [
			-72.09,
			41.3614
		]
	},
	"name" : "New London",
	"products" : [
		{
			"v" : 69.4,
			"t" : ISODate("2014-08-08T16:24:00Z"),
			"name" : "water_temperature",
			"f" : "0,0,0"
		},
		{
			"v" : 77,
			"t" : ISODate("2014-08-08T16:24:00Z"),
			"name" : "air_temperature",
			"f" : "0,0,0"
		},
		{
			"d" : "360.00",
			"g" : "8.75",
			"f" : "0,0",
			"s" : "4.08",
			"t" : ISODate("2014-08-08T16:24:00Z"),
			"dr" : "N",
			"name" : "wind"
		},
		{
			"v" : 1015.8,
			"t" : ISODate("2014-08-08T16:24:00Z"),
			"name" : "air_pressure",
			"f" : "0,0,0"
		}
	],
	"fetch_date" : ISODate("2014-08-08T16:37:22.640Z"),
	"id" : 8461490
}
```

If you would like just a dump file to play with, you can import the stations as well as the sensor data as well like this:
```
gunzip *.gz
mongoimport --host=<hostname> --port=<port> --username=<username> --password=<password> --db=<mydb> --collection=stations stations.json
mongoimport --host=<hostname> --port=<port> --username=<username> --password=<password> --db=<mydb> --collection=ocean_data ocean_data.json
```
