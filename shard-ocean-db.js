sh.enableSharding("ocean")
sh.shardCollection("ocean.ocean_data", {"station_id":1})
sh.shardCollection("ocean.stations", {"-ID":1})
