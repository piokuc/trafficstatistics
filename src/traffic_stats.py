#!/usr/bin/env python

"""
Implementaiton of the REST API using Flask.
"""

from flask import Flask, jsonify, make_response, abort, request
from collections import OrderedDict
import os
from html import html
from db import sql, traffic_columns
import config

app = Flask(__name__)
app.config.from_object(__name__)

def find_road(road):
    return [OrderedDict(zip(traffic_columns(), row)) for row in sql('select * from traffic where Road = ?', (road,))]

def qualified_columns():
    return ['traffic.' + c for c in traffic_columns()] + ['wards.ward', 'wards.district']

def find_ward(ward):
    s = 'select ' + ','.join(qualified_columns()) + \
        ''' from traffic, wards 
            where traffic.cp = wards.cp and wards.ward = ?
            order by AADFYear;
        '''
    names = traffic_columns() + ['ward', 'district']
    return [OrderedDict(zip(names,row)) for row in sql(s, (ward,))]

def find_records(criteria):
    def low(s): return set([e.lower() for e in s])
    def qualify(k):
        if k.lower() in low(traffic_columns()): return 'traffic.' + k
        elif k.lower() in low(['ward','district']): return 'wards.' + k

    # Only parameters that are known column names allowed
    if not low(criteria.keys()).issubset(low(traffic_columns() + ['ward','district'])):
        return None

    keys = criteria.keys()
    where = ' and '.join(qualify(k) + ' = ?' for k in keys)

    q = 'select ' + ','.join(qualified_columns()) + ' from traffic, wards '
    q += ' where traffic.cp = wards.cp ' 
    if where:
        q += ' and ' + where

    names = traffic_columns() + ['ward', 'district']
    params = tuple(criteria[k] for k in keys)
    return [OrderedDict(zip(names,row)) for row in sql(q, params)]

### Implementation of the API

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

@app.route('/api/v1.0/filter', methods=['GET'])
def filter():
    records = find_records(request.args.to_dict())
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
    return jsonify([r for r in sql('select distinct StartJunction,EndJunction from traffic order by 1,2')])

@app.route('/', methods=['GET'])
def documentation():
    def link(description, url): return description, html.a(href=url)(url)
    def ul(*lis): return html.ul(*[html.li(e) + '\n' for e in lis])
    return html.html(
        html.head(html.title('trafficstatistics.uk API documentation')),
        html.body(
            html.h1("Traffic statistics API examples"),
            ul(
               link("Browse data by road:",   "http://trafficstatistics.uk/api/v1.0/roads/M5"),
               link("Browse data by ward:",   "http://trafficstatistics.uk/api/v1.0/wards/Yeo"),
               link("Filter data according to criteria", 
                    "/api/v1.0/filter?EndJunction=Broadmeadow+Lane%2C+Teignmouth&StartJunction=A380%2FA383"),
               link("Get list of roads:",     "http://trafficstatistics.uk/api/v1.0/list/roads"),
               link("Get list of wards:",     "http://trafficstatistics.uk/api/v1.0/list/wards"),
               link("Get list of junctions:", "http://trafficstatistics.uk/api/v1.0/list/junctions")),
            "Author: ", html.a(href="http://kuchta.co.uk")("Peter Kuchta")
        ))

if __name__ == '__main__':
    app.run(**((not config.development_mode()) and {'host':'0.0.0.0','port':80} or {'debug':True}))
