
## A simple load test against the Ocean sample ##

This is a simple load test that can be run on this dataset.  It's designed to run a simple use case, and allow the user to scale up the load to test various components in MongoDB.

Initially there is a single use case:

- Get sensor data by station_id. The user selects all station entrys by id in order to fill out a graph over time. station_id (hashed) should be the shard key. This should be a local query. This is a index range scan, when multiple documents match the criteria. A random station id is selected per thread per execution. This should shred the crap out of the DB especially if it's not all in RAM. This is pure random I/O.

### Usage ###

See --help for usage, but it's very straightforward.

~~~ bash
$>python ./loadtest.py -u foo -p bar
~~~

This will launch 10 threads running against localhost:27017/ocean with the username, password specified.


__Credit to @too_many_bryans for the core code for greenlets.__
