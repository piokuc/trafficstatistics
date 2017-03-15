#!/usr/bin/env python

from flask import Flask, jsonify, make_response, abort
from contextlib import closing
import sqlite3

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

def column_names():
    with closing(connect_db()) as conn:
        cur = conn.cursor()
        cur.execute('PRAGMA table_info(traffic);')
        return [ci[1] for ci in cur.fetchall()]

def find_road(road):
    names = column_names()
    with closing(connect_db()) as conn:
        cur = conn.cursor()
        cur.execute('select * from traffic where Road = ?', (road,))
        return [dict(zip(names, row)) for row in cur.fetchall()]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404) 

@app.route('/traffic_stats/api/v1.0/roads/<string:road>', methods=['GET'])
def index(road):
    records = find_road(road)
    if not records:
        abort(404)
    return jsonify(records)


if __name__ == '__main__':
    app.run(debug=True)
