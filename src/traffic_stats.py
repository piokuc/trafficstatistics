#!/usr/bin/env python

from flask import Flask, jsonify, make_response, abort
from contextlib import closing
from collections import OrderedDict
import sqlite3
import os

# configuration
#DATABASE = ':memory:'
DATABASE = '/tmp/traffic.sqlite'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db(): 
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    try:
        with closing(connect_db()) as conn:
            with app.open_resource('traffic.sql', mode='r') as f:
                script = f.read()
                conn.cursor().executescript(script)
            conn.commit()
    except sqlite3.OperationalError as e:
        assert 'already exists' in e.message 

init_db()

def sql(*args):
    with closing(connect_db()) as conn:
        cur = conn.cursor()
        cur.execute(*args)
        return cur.fetchall()

def column_names():
    return [ci[1] for ci in sql('PRAGMA table_info(traffic);')]

def find_road(road):
    return [OrderedDict(zip(column_names(), row)) for row in sql('select * from traffic where Road = ?', (road,))]

def find_ward(ward):
    traffic_names = column_names()
    names = traffic_names + ['ward', 'district']
    qualified_names = ['traffic.' + c for c in column_names()] + ['ward', 'district']
    s = 'select ' + ','.join(qualified_names) + \
        ''' from traffic, wards 
            where traffic.cp == wards.cp and wards.ward = ?
            order by AADFYear;
        '''
    return [OrderedDict(zip(names,row)) for row in sql(s, (ward,))]
    

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404) 

@app.route('/api/v1.0/roads/<string:road>', methods=['GET'])
def roads(road):
    records = find_road(road)
    if not records: abort(404)
    return jsonify(records)

@app.route('/api/v1.0/wards/<string:ward>', methods=['GET'])
def wards(ward):
    records = find_ward(ward)
    if not records: abort(404)
    return jsonify(records)

@app.route('/api/v1.0/list/roads', methods=['GET'])
def list_roads():
    return jsonify([r[0] for r in sql('select distinct Road from traffic')])
    
@app.route('/api/v1.0/list/wards', methods=['GET'])
def list_wards():
    return jsonify([r[0] for r in sql('select distinct ward from wards')])

@app.route('/', methods=['GET'])
def documentation():
    return """
    <html>
    <head><title>trafficstatistics.uk API documentation</title></head>

    <body>

    <h1> Examples </h1>

    <ul>
    <li> Browse data by road:
    <a href="http://trafficstatistics.uk/api/v1.0/roads/M5">http://trafficstatistics.uk/api/v1.0/roads/M5</a>
    </li>

    <li> Browse data by ward:
    <a href="http://trafficstatistics.uk/api/v1.0/wards/Yeo">http://trafficstatistics.uk/api/v1.0/wards/Yeo</a>
    </li>

    <li> Get list of roads:
    <a href="http://trafficstatistics.uk/api/v1.0/list/roads">http://trafficstatistics.uk/api/v1.0/list/roads</a>
    </li>

    <li> Get list of wards:
    <a href="http://trafficstatistics.uk/api/v1.0/list/wards">http://trafficstatistics.uk/api/v1.0/list/wards</a>
    </li>


    </ul>
    </body>

    </html>
    """

if __name__ == '__main__':
    app.run(**(('redhat' in os.getenv('MACHTYPE')) and {'host':'0.0.0.0','port':80} or {'debug':True}))
