# API for browsing  traffic count and major road data #

### Server code and documentation of API ###

The links below all give information on traffic count and major road data. 

* Data:           http://api.dft.gov.uk/v2/trafficcounts/export/la/Devon.csv
* Metadata:       http://data.dft.gov.uk/gb-traffic-matrix/aadf-majorroads-metadata.pdf
* General info:   https://www.dft.gov.uk/traffic-counts/about.php

We would like you to create (and deploy) a web service that allows a user to navigate this data.

* The data is public so no authentication is required.
* The client will be one or more of python, javascript, curl
* The API structure is up to you
* Use python for the server
* Use postgres for the database if you need one
* We will need able to use it so some form of documentation will be required

For extra credit (if you have time), allow to client to navigate the data by ward using boundaries defined here: 

https://tinyurl.com/gvlj4so   (zipfile)

with an explanation of the fields here:  
https://tinyurl.com/zozxpfb

FAQ

* Do I need to host it myself?: Yes, AWS, azure etc all offer free tiers. It will only need to be up for a week
* Do I need to build a client?:  No, we’re only after an API. 
* Do you need the code?:  Yes please, we would like to review it. Github, bitbucket, zipfile are all acceptable 


### API Documentation ###

The traffic statistics REST API http://trafficstatistics.uk/ 
provides read only access to annual average daily flow (AADF) data 
available from [Department for Transport](https://www.dft.gov.uk/traffic-counts/about.php).

Currently it serves only [Devon](http://api.dft.gov.uk/v2/trafficcounts/export/la/Devon.csv data).

Full description of the orignal dataset's metadata is described [here](http://data.dft.gov.uk/gb-traffic-matrix/aadf-majorroads-metadata.pdf)

API is read only and does not require any authentication. Only GET method is supported.

All APIs apart from /api/v1.0/list/{roads|wards|junctions} 
return list of dictionaries in the JSON format, 
with keys being column names of the original CSV 
file and values corresponding to values in appropriate rows.
Four additional keys are added: ward, district, latitude and longitude.

Currently the only possible error code of all API calls is `404 Not found`.
```
{
      "error": "Not found"
}
```

**Filter**
----
  Returns JSON encoded records satisfying given criteria.

* **URL**

    `/api/v1.0/filter`

*  **URL Params**

The only allowed parameters are the ones appearing in the dataset's metadata table above.
Result will be a list of records that match the parameters.

*  **Example**
` $ curl "http://trafficstatistics.uk/api/v1.0/filter?AADFYear=2015&ward=Yarty"`
                                 
* **Code:** `200` 
**Content:** 
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





### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Author: Piotr Kuchta, peter@kuchta.co.uk
