db.ocean_data.aggregate(
    { $unwind : "$products" },
    { $group: {
      _id:"$products.name", theavg: { $avg:"$products.v" }
      }
    });


// get averages grouped by name
db.ocean_data.aggregate(
    [
        { $unwind : "$products" },
        { $group: { _id:"$products.name", theavg: { $avg:"$products.v" } } }
    ]
 );

// get average values group by year, and by product
 db.ocean_data.aggregate(
   [
       { $unwind : "$products" },
       {
           $project: {
               "name": 1,
               "products.t" : 1,
               "products.v" : 1,
               "products.name" : 1,
               "theyear" : { "$year": "$products.t" }
           }
       },
       { $group: {
           _id: {
               "year":"$theyear",
               "name":"$products.name"
            },
            theavg: {
                $avg:"$products.v" }
            }
        }
   ]
);

// get average values group by year, and by product, where product = water temp
 db.ocean_data.aggregate(
   [
       { $unwind : "$products" },
       { $match: {"products.name":"water_temperature"}},
       {
           $project: {
               "name": 1,
               "products.t" : 1,
               "products.v" : 1,
               "products.name" : 1,
               "theyear" : { "$year": "$products.t" }
           }
       },
       { $group: {
           _id: {
               "year":"$theyear",
               "name":"$products.name"
            },
            theavg: {
                $avg:"$products.v" }
            }
        }
   ]
);

// get average values group by year, and by product
 db.ocean_data.aggregate(
   [
       { $unwind : "$products" },
       {
           $project: {
               "name": 1,
               "products.t" : 1,
               "products.v" : 1,
               "products.name" : 1,
               "theyear" : { "$year": "$products.t" }
           }
       },
       { $group: {
           _id: {
               "year":"$theyear"
            },
            thecount: {
                $sum:1 }
            }
        }
   ]
);

// add geo into the mix
db.ocean_data.aggregate(
    [
        { $geoNear: {
           near: { type: "Point", coordinates: [ -117.1572600, 32.7153300 ] },
           distanceField: "dist.calculated",
           includeLocs: "dist.location",
           num: 5,
           spherical: true
        }},
        { $unwind : "$products" },
        { $match: {"products.name":"water_temperature"}},
        {
          $project: {
              "name": 1,
              "products.t" : 1,
              "products.v" : 1,
              "products.name" : 1,
              "theyear" : { "$year": "$products.t" }
          }
        },
        { $group: {
            _id: { "year":"$theyear" },
            station: { $max:"$name"},
            product: { $max:"$products.name" },
            theavg: { $avg:"$products.v" }
           }
        }
    ]
);
