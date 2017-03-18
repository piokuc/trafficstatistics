#!/usr/bin/env python

from flask import Flask, jsonify, make_response, abort
from contextlib import closing
from collections import OrderedDict
import sqlite3
import os
from html import html

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
    qualified_names = ['traffic.' + c for c in traffic_names] + ['ward', 'district']
    s = 'select ' + ','.join(qualified_names) + \
        ''' from traffic, wards 
            where traffic.cp == wards.cp and wards.ward = ?
            order by AADFYear;
        '''
    names = traffic_names + ['ward', 'district']
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

@app.route('/api/v1.0/list/junctions', methods=['GET'])
def list_junctions():
    return jsonify([r for r in sql('select distinct StartJunction,EndJunction from traffic where StartJunction is not NULL and EndJunction is not NULL order by 1,2')])

def link(description, url): return description, html.a(href=url)(url)
def ul(*lis): return html.ul(*[html.li(e) + '\n' for e in lis])

@app.route('/', methods=['GET'])
def documentation():
    return html.html(
        html.head(html.title('trafficstatistics.uk API documentation')),
        html.body(html.h1("Traffic statistics API Examples"),
            ul(
               link("Browse data by road:",   "http://trafficstatistics.uk/api/v1.0/roads/M5"),
               link("Browse data by ward:",   "http://trafficstatistics.uk/api/v1.0/wards/Yeo"),
               link("Get list of roads:",     "http://trafficstatistics.uk/api/v1.0/list/roads"),
               link("Get list of wards:",     "http://trafficstatistics.uk/api/v1.0/list/wards"),
               link("Get list of junctions:", "http://trafficstatistics.uk/api/v1.0/list/junctions"))))

if __name__ == '__main__':
    app.run(**((not os.getenv('EDITOR')) and {'host':'0.0.0.0','port':80} or {'debug':True}))
