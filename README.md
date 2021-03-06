# API for browsing traffic counts and major road data #

## General information ##

The traffic statistics REST API http://trafficstatistics.uk/ 
provides read only access to annual average daily flow (AADF) data 
available from [Department for Transport](https://www.dft.gov.uk/traffic-counts/about.php).
Currently it serves only [Devon data](http://api.dft.gov.uk/v2/trafficcounts/export/la/Devon.csv).
Full description of the orignal dataset's metadata is described [here](http://data.dft.gov.uk/gb-traffic-matrix/aadf-majorroads-metadata.pdf)

API is read only and does not require any authentication. Only GET method is supported.

All APIs apart from `/api/v1.0/list/{roads|wards|junctions}`
return list of dictionaries in the JSON format, 
with keys being column names of the original CSV 
file and values corresponding to values in appropriate rows.
Four additional keys are added: ward, district, latitude and longitude.

## Error codes ##
Currently the only possible error code of all API calls is `404 Not found`.
```
{
      "error": "Not found"
}
```

-----------------------
*Filter records according to criteria*
----
  Returns JSON encoded records satisfying given criteria.

* **URL**

    `/api/v1.0/filter`

* **URL Parameters**

None, the filter API accepts only query parameters.

* **Query Parameters**

The only allowed parameters are the ones appearing in the dataset's metadata table below.
Result will be a list of records that match the parameters.

Parameter name  | Description
----------------|-------------------------
AADFYear        | AADFs are shown for each year from 2000 onwards. 
CP (count point) | a unique  reference  for the road link that links  the  AADFs to the  road network. 
Estimation_method | Estimation method 
Estimation_method_detailed | Detailed description of the estimation method 
LocalAuthority | Local authority  that the CP sits within
Road | this is the  road name  (for instance  M25 or A3) 
RoadCategory | the  classification of the  road type  (see data definitions for the full  list). 
Easting | Easting coordinates of the CP location. 
Northing | Northing coordinates of the CP location. 
StartJunction | The  road name of the  start junction  of the  link 
EndJunction | The  road name of the  end junction  of the  link 
LinkLength_km | Total length  of the  network  road link for that CP (in kilometres). 
LinkLength_miles| Total length  of the network  road link  for that CP (in miles). 
PedalCycles | AADF for pedal cycles. 
Motorcycles | AADF for two-wheeled  motor vehicles. 
CarsTaxi | AADF for Cars and Taxis. 
BusesCoaches | AADF for Buses and Coaches 
LightGoodsVehicles | AADF for LGVs. 
V2AxleRigidHGV | AADF for two-rigid axle  HGVs. 
V3AxleRigidHGV | AADF for three-rigid axle  HGVs. 
V4or5AxleRigidHGV | AADF for four or more rigid axle  HGVs. 
V3or4AxleArticHGV | AADF for three  or four-articulated  axle HGVs. 
V5AxleArticHGV | AADF for five-articulated  axle  HGVs. 
V6orMoreAxleArticHGV | AADF for six-articulated  axle  HGVs. 
AllHGVs | AADF for all HGVs. 
AllMotorVehicles | AADF for all motor vehicles. 
ward     | ward
district | district
latitude | latitude
longitude | longitude 

* ** Example **

    ` $ curl "http://trafficstatistics.uk/api/v1.0/filter?AADFYear=2015&ward=Yarty"`
                                 
* ** Code ** 

    `200` 

* ** Response ** 

```
[
  {
    "AADFYear": 2015, 
    "AllHGVs": 142, 
    "AllMotorVehicles": 2127, 
    "BusesCoaches": 11, 
    "CP": 48236, 
    "CarsTaxis": 1525, 
    "Easting": 325000, 
    "EndJunction": "A358 Furnham Road", 
    "Estimation_method": "Estimated", 
    "Estimation_method_detailed": "Estimated using previous year's AADF on this link", 
    "LightGoodsVehicles": 432, 
    "LinkLength_km": 6.1, 
    "LinkLength_miles": 3.79, 
    "LocalAuthority": "Devon", 
    "Motorcycles": 17, 
    "Northing": 107972, 
    "PedalCycles": 10, 
    "Region": "South West", 
    "Road": "A30", 
    "RoadCategory": "PR", 
    "StartJunction": "A303", 
    "V2AxleRigidHGV": 73, 
    "V3AxleRigidHGV": 28, 
    "V3or4AxleArticHGV": 3, 
    "V4or5AxleRigidHGV": 8, 
    "V5AxleArticHGV": 6, 
    "V6orMoreAxleArticHGV": 24, 
    "district": "East Devon", 
    "latitude": 50.8663681243184, 
    "longitude": -3.06713124536112, 
    "ward": "Yarty"
  }, 
  {
    "AADFYear": 2015, 
    "AllHGVs": 852, 
    "AllMotorVehicles": 13208, 
    "BusesCoaches": 31, 
    "CP": 73394, 
    "CarsTaxis": 10398, 
    "Easting": 324774, 
    "EndJunction": "LA Boundary", 
    "Estimation_method": "Counted", 
    "Estimation_method_detailed": "Dependent on a neighbouring counted link", 
    "LightGoodsVehicles": 1846, 
    "LinkLength_km": 2.9, 
    "LinkLength_miles": 1.8, 
    "LocalAuthority": "Devon", 
    "Motorcycles": 81, 
    "Northing": 110375, 
    "PedalCycles": 0, 
    "Region": "South West", 
    "Road": "A303", 
    "RoadCategory": "TR", 
    "StartJunction": "B3170", 
    "V2AxleRigidHGV": 289, 
    "V3AxleRigidHGV": 61, 
    "V3or4AxleArticHGV": 82, 
    "V4or5AxleRigidHGV": 71, 
    "V5AxleArticHGV": 190, 
    "V6orMoreAxleArticHGV": 159, 
    "district": "East Devon", 
    "latitude": 50.8879437395178, 
    "longitude": -3.07083733470763, 
    "ward": "Yarty"
  }
]
```



-----------------------
*Browse traffic statistics by roads*
----
  Returns JSON encoded records for the given road. The format of the result is the same as for the filter API.

* **URL**

    `/api/v1.0/roads/{road}`

* **URL Parameters**

    `road` should be one of the roads available via [/api/v1.0/list/roads](http://trafficstatistics.uk/api/v1.0/list/roads)

* **Query Parameters**

    None.

* ** Example **

    `$ curl "http://trafficstatistics.uk/api/v1.0/roads/M5" `
                                 
* ** Code ** 

    `200` 

* ** Response ** 

Simillar to the example response for the Filter API, see above.


-----------------------
*Browse traffic statistics by wards*
----
  Returns JSON encoded records for the given ward. The format of the result is the same as for the filter API.

* ** URL **

    `/api/v1.0/wards/{ward}`

* ** URL Parameters **

    `ward` should be one of the wards availble via [/api/v1.0/list/wards](http://trafficstatistics.uk/api/v1.0/list/wards)

* ** Query Parameters **

    None.

* ** Example **

    `$ curl http://trafficstatistics.uk/api/v1.0/wards/Chulmleigh`
                                 
* ** Code ** 

    `200` 

* ** Response ** 

Simillar to the example response for the Filter API, see above.


-----------------------
*Get list of major roads*
----
  Returns JSON encoded list of major roads.

* ** URL **

    `/api/v1.0/list/roads`

* ** URL Parameters **

    None

* ** Query Parameters **

    None.

* ** Example **

    `$ curl http://trafficstatistics.uk/api/v1.0/list/roads`
                                 
* ** Code ** 

    `200` 

* ** Response ** 

```
[
    "A358", 
    "A3126", 
    "A3121", 
    "A386", 
    "A3123", 
    "A384", 
    "A379", 
    "A38", 
    "A3125", 
    "A377", 
    "A3122", 
    "A396", 
    "A3124", 
    "A3015", 
    "A383", 
    "A382", 
    "A35", 
    "A399", 
    "A303", 
    "A385", 
    "A388", 
    "A381", 
    "M5", 
    "A30", 
    "A390", 
    "A39", 
    "A3052", 
    "A375", 
    "A373", 
    "A361", 
    "A3072", 
    "A380", 
    "A376", 
    "A3079"
]

```


-----------------------
*Get list of wards*
----
  Returns JSON encoded list of known wards.

* ** URL **

    `/api/v1.0/list/wards`

* ** URL Parameters **

    None

* ** Query Parameters **

    None.

* ** Example **

    `$ curl http://trafficstatistics.uk/api/v1.0/list/wards`
                                 
* ** Code ** 

    `200` 

* ** Response ** 

[Shortened]

```
[
    "Instow", 
    "Axminster Town", 
    "Cranmore", 
    "Okehampton North", 
    "Chudleigh", 
    "Coly Valley", 
    "Georgeham and Mortehoe", 
    "Westexe", 
    "Newport", 
    "Burrator", 
    "Pilton", 
    "Haytor", 
    "Witheridge", 
    "Cadbury", 
    "Bradley", 
    "Monkleigh and Littleham", 
    "College", 
    "Exe Valley"
]

```


-----------------------
*Get list of junctions*
----
  Returns JSON encoded list of pairs: (StartJunction, EndJunction).

* ** URL **

    `/api/v1.0/list/junctions`

* ** URL Parameters **

    None

* ** Query Parameters **

    None.

* ** Example **

    `$ curl http://trafficstatistics.uk/api/v1.0/list/junctions`
                                 
* ** Code ** 

    `200` 

* ** Response ** 

[Shortened]

```
[
  [
    "Sannerville Way Rndbt", 
    "Glasshouse Lane"
  ], 
  [
    "Sidmouth", 
    "A3052"
  ], 
  [
    "Station Rd", 
    "A30 slip roads mid-junction"
  ], 
  [
    "Stoke Hill", 
    "A3072"
  ], 
  [
    "Summer Lane", 
    "B3179"
  ], 
  [
    "Tamerton Rd roundabout", 
    "B3212 roundabout"
  ], 
  [
    "Tamerton Road roundabout", 
    "B3212 roundabout"
  ], 
  [
    "Telegraph Hill", 
    "A38"
  ], 
  [
    "Telegraph  Hill", 
    "A38"
  ], 
  [
    "Westaway Plain", 
    "B3230"
  ], 
  [
    "Whiddon Drive", 
    "A361"
  ], 
  [
    "Whiddon Drive", 
    "A39(T)"
  ]
]
```
-----------------------

### How do I get set up? ###

* Summary of set up

The web app can run with sqlite3 and PostgreSQL. 
Currently PostgreSQL is used in the production on an ec2 instance, sqlite3 in development and testing.

The source code contains dump of the sqlite3 database in file `src/traffic.sql`.
In development mode the app will load `src/traffic.sql` and create database in file `/tmp/traffic.sqlite` unless it already exists.

* Configuration

The app detects if it is in development or production mode based on value returned from function `development_mode` in module `src/config.py`.

In my setup this is based on whether environment contains variable `EDITOR` or not (the variable is not set on ec2).
This needs to be ammended according to local set up.

* Dependencies

Python module dependencies are listed in file `requirements.txt`.
In production mode the app requires installed and running PostgreSQL. 

* Database configuration

The initial conversion of the CSV file to sqlite3 database was done with an online tool.
The script `load_wards.py` creates an additional table `wards`.

The script `sqlite3_to_postgresql.sh` can convert the sqlite3 dump of the database to a format that can be loaded into a PostgreSQL database.
Details of the PostgreSQL database connection should be put in file PG_CONNECTION (not in source code repository).

Note, most of the data is in one flat table. 
It would be good to normalize the schema. 
However, the data must be cleaned up first.
There are numerous inconsistencies in the original dataset,
like different spellings of the same road or junction,
inconsistent use of abbreviations as well as ordinary typos.
Some considerable effort is needed to clean up the data. 
However, cleaning the data and redesigning the database should not 
require any changes to the API and only small changes to the application's logic (SQL queries).

* How to run tests

Unit tests are in module `test.py`. To run the suite:

```
$ cd src
$ python test.py
```

* Deployment instructions

The simplest way to run the app in development mode is:

```
$ python traffic_stats.py
```

### Who do I talk to? ###

* Author: Piotr Kuchta, peter@kuchta.co.uk
