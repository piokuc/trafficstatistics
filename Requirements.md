# API for browsing  traffic count and major road data #

### Requirements for server code and documentation of API ###

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

