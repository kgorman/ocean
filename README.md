## Ocean

### Overview
Ocean exists to populate a sample MongoDB dataset with NOAA data for usage in examples, teaching, etc.  This dataset is naturally suited for MongoDB and thus a perfect candidate.  The data is pulled from the API and normalized slightly to ensure easy queryability.

This dataset has some nice native properties
- Density.  Fetching all 'products' is a single document fetch and likely 3 I/O's max.
- Shardability.  Sharding on station_id (HASHED) works really nicely.
- Geo.  Lat/Lon index for doing any geo queries.

The data is pulled via http://tidesandcurrents.noaa.gov/api/

### Installation

This is a stand alone python script.

Requirements:
- requests
- pymongo

You can run this on the command line like:

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
    "_id" : ObjectId("537a32e9d211f0061b91c9b1"),
    "station_id" : "8454049",
    "name" : "Quonset Point",
    "lon" : "-71.4110",
    "products" : [
        {
            "data" : [
                {
                    "f" : "0,0,0",
                    "t" : "2014-05-19 16:30",
                    "v" : "57.6"
                }
            ],
            "name" : "water_temperature"
        },
        {
            "data" : [
                {
                    "f" : "0,0,0",
                    "t" : "2014-05-19 16:30",
                    "v" : "62.8"
                }
            ],
            "name" : "air_temperature"
        },
        {
            "data" : [
                {
                    "d" : "317.00",
                    "g" : "14.97",
                    "f" : "0,0",
                    "s" : "11.66",
                    "t" : "2014-05-19 16:30",
                    "dr" : "NW"
                }
            ],
            "name" : "wind"
        },
        {
            "data" : [
                {
                    "f" : "0,0,0",
                    "t" : "2014-05-19 16:30",
                    "v" : "1017.2"
                }
            ],
            "name" : "air_pressure"
        },
        {
            "data" : [
                {
                    "s" : "27.30",
                    "t" : "2014-05-19 16:30",
                    "g" : "1.021"
                }
            ],
            "name" : "salinity"
        }
    ],
    "lat" : "41.5868",
    "fetch_date" : ISODate("2014-05-19T11:35:52.414Z"),
    "id" : "8454049"
}
```
