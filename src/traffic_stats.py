#!/usr/bin/env python

from flask import Flask, jsonify, make_response, abort
from collections import OrderedDict
import os
from html import html
from db import sql, traffic_columns

app = Flask(__name__)
app.config.from_object(__name__)

def find_road(road):
    return [OrderedDict(zip(traffic_columns(), row)) for row in sql('select * from traffic where Road = ?', (road,))]

def find_ward(ward):
    traffic_names = traffic_columns()
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
    return jsonify([r for r in sql('select distinct StartJunction,EndJunction from traffic order by 1,2')])

def link(description, url): return description, html.a(href=url)(url)
def ul(*lis): return html.ul(*[html.li(e) + '\n' for e in lis])

@app.route('/', methods=['GET'])
def documentation():
    return html.html(
        html.head(html.title('trafficstatistics.uk API documentation')),
        html.body(
            html.h1("Traffic statistics API examples"),
            ul(
               link("Browse data by road:",   "http://trafficstatistics.uk/api/v1.0/roads/M5"),
               link("Browse data by ward:",   "http://trafficstatistics.uk/api/v1.0/wards/Yeo"),
               link("Get list of roads:",     "http://trafficstatistics.uk/api/v1.0/list/roads"),
               link("Get list of wards:",     "http://trafficstatistics.uk/api/v1.0/list/wards"),
               link("Get list of junctions:", "http://trafficstatistics.uk/api/v1.0/list/junctions")),
            "Author: ", html.a(href="http://kuchta.co.uk")("Peter Kuchta")
        ))

if __name__ == '__main__':
    app.run(**((not os.getenv('EDITOR')) and {'host':'0.0.0.0','port':80} or {'debug':True}))
