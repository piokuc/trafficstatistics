#!/usr/bin/env python

from flask import Flask
import sqlite3
from contextlib import closing

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
    

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
